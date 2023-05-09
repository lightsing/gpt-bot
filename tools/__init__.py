import json

import openai
from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer

from .food import gen_food
from .yunshi import gen_yunshi
from .nonsense import gen_nonsense

logger = logging.getLogger("bot")

@cached(
    cache=Cache.REDIS,
    ttl=3600,
    serializer=JsonSerializer(),
    namespace="route",
    skip_cache_func=lambda r: r is None
)
async def route(req: str):
    prompt = """根据用户的输入，判断要调用哪个函数。你可以调用的函数有：
1. 日常问候 gen_greeting
2. 今日运势 gen_yunshi
3. 今日食物 gen_food
4. 给用户起名 gen_naming
5. 除外的任何其他情况下都输出 gen_nonsense
例如：
{"user_msg": "早上好"} 输出：{"action": "gen_greeting"}
{"user_msg": "晚安"} 输出：{"action": "gen_greeting"}
{"user_msg": "今晚吃什么"} 输出：{"action": "gen_food"}
{"user_msg": "你打算叫我什么"} 输出：{"action": "gen_naming"}
{"user_msg": "帮我起个昵称"} 输出：{"action": "gen_naming"}
{"user_msg": "嘿！"} 输出：{"action": "gen_nonsense"}
{"user_msg": "张三可以吃吗"} 输出：{"action": "gen_nonsense"}
"""
    temperature = 0.1
    max_tokens = 10

    for _ in range(10):
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            temperature=temperature,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": req}
            ],
            max_tokens=max_tokens,
            n=1,
        )
        choice = completion['choices'][0]['message']['content']
        logger.info(f'cache miss for {req}, raw choice: {choice}')
        try:
            return json.loads(choice)["action"]
        except Exception as e:
            logger.warn(f"error occur when processing {e}")

    return None


async def route_mapping(req: str):
    choice = await route(req)
    logger.info(f'choose tool {choice} for {req}')
    try:
        return globals()[choice]
    except KeyError:
        return gen_nonsense
