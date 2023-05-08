import openai


async def gen_yunshi(req: str):
    prompt = """用户会输入类似“今日运势”的询问，你会生成一些很荒谬搞笑的类似今日运势格式的文字，除此以外不要回复多余的文字。
例如：
今天你的运势格外奇特，穿一只左脚袜子可能会带来好运，遇到困难时对着电风扇喊5遍“我是霸王龙”，让问题迎刃而解。午餐选择吃三明治，但要将里面的肉夹在面包外面。下班途中遇到拱桥可以顺手摸三下栏杆，晚上回家后将枕头调换位置将带来一个甜美的梦境。
今天你与大自然的关系格外融洽，穿上绿色裤子，可以秒变场上最靓的仔。午餐时间，尝试和盆栽植物合影来提升好运指数。上班时遇到困难，蹲下来跟自己的鞋子交流一下，说不定会迎来灵感。结束一天的忙碌，请记得带一叶子回家，捧在手里舞动一番，提神醒脑之余还能瘦小腿！
今天贵人星高照，建议穿上拖鞋去见老板，说不定会加薪。午餐时要小心口袋里的黄瓜，它可能会跳出来引起尴尬。感情方面，朋友圈发一条英文句子就能得到他人的追求。今晚走路去月球，遇见三头狮子与其共舞，智慧大增。记得走路时跳踢踏舞，途中捡到的钱财都是你的哦！
"""
    temperature = 1.3
    presence_penalty = 0.1
    max_tokens = 250

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
    )

    return completion['choices'][0]['message']['content']
