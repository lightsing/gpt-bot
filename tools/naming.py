import json

import openai
from mirai import MessageEvent

from .log import get_logger
from .helper import event_to_trace_id, event_to_system, set_name_by_event, get_name_by_event

logger = get_logger("naming")


async def gen_naming(req: str, event: MessageEvent):
    prompt = """根据输入的JSON，自主决定给用户取一个昵称。仅输出JSON内容。
例子：
{"user_msg": "给我想个昵称", "current_name": "荒海安邪良", "username": "荒海安邪良"}；输出：{"message": "我决定叫你阿邪！", "set": "阿邪"}
{"user_msg": "我不喜欢这个名字，重新给我取一个昵称吧", "current_name": "饭", "username": "饭"}；输出：{"message": "那叫你饭饭吧~", "set": "饭饭"}
{"user_msg": "重新给我取一个昵称吧", "current_name": "饭饭", "username": "饭"}；输出：{"message": "hmmm 那叫你阿饭", "set": "阿饭"}
"""

    max_tokens = 100
    for _ in range(10):
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "system", "content": event_to_system(event)},
                {"role": "user", "content": json.dumps({
                    "user_msg": req,
                    "current_name": get_name_by_event(event),
                    "username": event.sender.get_name(),
                })}
            ],
            max_tokens=max_tokens,
            n=1,
            user=event_to_trace_id(event)
        )
        choice = completion['choices'][0]['message']['content']

        logger.info(f"completion: {choice}")
        try:
            action = json.loads(choice)
            set_name_by_event(action["set"], event)
            return action["message"]
        except Exception as e:
            logger.info(e)
            continue

    return "改天再说，很忙"
