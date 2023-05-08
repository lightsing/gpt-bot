from functools import lru_cache

import openai

from .food import gen_food
from .yunshi import gen_yunshi
from .nonsense import gen_nonsense


@lru_cache(maxsize=1000)
def route(req: str):
    prompt = """根据用户的输入，判断要调用哪个函数。你可以调用的函数有：
1. 今日运势 gen_yunshi
2. 今日食物 gen_food
4. 除外的任何其他情况下都输出 gen_nonsense
请返回函数名，不要输出其他东西。
例如：
用户：今晚吃什么；输出：gen_food
用户：嘿！；输出：gen_nonsense
用户：张三可以吃吗；输出：gen_nonsense
"""
    temperature = 0.1
    max_tokens = 10

    completion = openai.ChatCompletion.create(
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
    choice = choice.encode("ascii", errors="ignore").decode()

    return choice