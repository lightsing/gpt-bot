import asyncio
import logging

import openai
from mirai import Mirai, GroupMessage, MiraiRunner
from mirai.models import At, Plain

from config import OPENAI_API_KEY, BOT_ID, ADAPTER
from tools import gen_food, gen_yunshi, gen_nonsense, route_mapping

openai.api_key = OPENAI_API_KEY

logging.basicConfig()
logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)


def main():
    bot = Mirai(qq=BOT_ID, adapter=ADAPTER)

    work = asyncio.Queue()

    async def handle_message():
        while True:
            try:
                event, req = await work.get()
                route = await route_mapping(req)
                ret = await route(req)
                logger.info(f'[bot] send message {ret}')
                await bot.send(
                    event,
                    [Plain(ret)],
                    True
                )
            except Exception as e:
                logger.error(e)

    @bot.on(GroupMessage)
    async def on_group_message(event: GroupMessage):
        try:
            message_chain = event.message_chain
            if not At(bot.qq) in message_chain:
                return
            if not Plain in message_chain:
                return
            content = message_chain.get(Plain)
            logger.info(f'[bot] receive message {content}')
            await work.put((event, str(content).strip()))
        except Exception as e:
            logger.error(e)

    runner = MiraiRunner(bot)

    loop = asyncio.get_event_loop()
    loop.create_task(runner._run())
    loop.create_task(handle_message())
    loop.run_forever()


if __name__ == "__main__":
    main()
