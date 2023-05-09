import asyncio
import logging

import openai

from config import OPENAI_API_KEY
from rqueue import PersistentQueue
from tools import route_mapping

openai.api_key = OPENAI_API_KEY
openai.log = 'info'

logging.basicConfig()
logger = logging.getLogger("ai")
logger.setLevel(logging.INFO)


async def main():
    incoming_queue = PersistentQueue('incoming')
    sending_queue = PersistentQueue('outgoing')

    while True:
        try:
            event, req = await incoming_queue.pop()
            logger.info(f'received request: {req}')
            route = await route_mapping(req)
            ret = await route(req, event)
            logger.info(f'generated response: {ret}')
            await sending_queue.push(
                (
                    event.sender.group.id,
                    ret,
                    event.message_chain.message_id,
                )
            )
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    asyncio.run(main())
