import openai


async def gen_nonsense(req: str):
    prompt = """你是一个群机器人，你会根据用户的输入，以荒谬的、没有逻辑的话语拒绝用户的输入。"""

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
    )
    choice = completion['choices'][0]['message']['content']

    return choice
