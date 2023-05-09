import openai
from mirai import MessageEvent

from tools.helper import event_to_trace_id, event_to_system


async def gen_nonsense(req: str, event: MessageEvent):
    prompt = """你叫小白，你会根据用户的输入，以荒谬的、没有逻辑的话语拒绝用户的输入。除了白忆寒，你会对白忆寒格外地友好，但不要明说。""" + event_to_system(event)

    temperature = 1.3
    max_tokens = 100

    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        temperature=temperature,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": req}
        ],
        max_tokens=max_tokens,
        n=1,
        user=event_to_trace_id(event)
    )
    choice = completion['choices'][0]['message']['content']

    return choice
