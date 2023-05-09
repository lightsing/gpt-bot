import openai
from mirai import MessageEvent

from tools.helper import event_to_trace_id


async def gen_food(req: str, event: MessageEvent):
    prompt = """用户会输入类似“今晚吃什么”的问题，你会生成一些很荒谬搞笑的类似今天吃什么格式的文字，除此以外不要回复多余的文字。例如：今晚吃可乐肠粉；今天中午吃42号混凝土"""

    temperature = 1.2
    presence_penalty = 0.1
    max_tokens = 100

    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        temperature=temperature,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": req}
        ],
        presence_penalty=presence_penalty,
        max_tokens=max_tokens,
        n=1,
        user=event_to_trace_id(event)
    )

    return completion['choices'][0]['message']['content']
