import asyncio
import logging

from mirai import Mirai, GroupMessage, MiraiRunner
from mirai.models import At, Plain

from config import BOT_ID, ADAPTER
from rqueue import PersistentQueue

logging.basicConfig()
logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)


def main():
    bot = Mirai(qq=BOT_ID, adapter=ADAPTER)
    incoming_queue = PersistentQueue('incoming')
    sending_queue = PersistentQueue('outgoing')

    async def sending_message():
        while True:
            try:
                _id, message, quoting = await sending_queue.pop()
                logger.info(f'send message {message}')
                await bot.send_group_message(
                    target=_id,
                    message_chain=[Plain(message)],
                    quote=quoting
                )
            except Exception as e:
                logger.error(e)

    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        try:
            message_chain = event.message_chain
            if At(bot.qq) not in message_chain:
                return
            if Plain not in message_chain:
                return
            content = message_chain.get_first(Plain)
            logger.info(f'[bot] receive message {content}')
            await incoming_queue.push((event, content.text.strip()))
        except Exception as e:
            logger.error(e)

    runner = MiraiRunner(bot)

    loop = asyncio.get_event_loop()
    loop.create_task(runner._run())
    loop.create_task(sending_message())
    loop.run_forever()


if __name__ == "__main__":
    main()
