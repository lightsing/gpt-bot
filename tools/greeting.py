import json
import time

import openai
from mirai import MessageEvent

from .log import get_logger
from .helper import event_to_trace_id, event_to_system, set_name_by_event, get_name_by_event

logger = get_logger("greeting")


async def gen_greeting(req: str, event: MessageEvent):
    prompt = "对用户的问候语进行适当的回应，当用户在不合适的时间发送互动时（例如下午发送早上好），对用户进行嘲笑。" \
             + event_to_system(event) \
             + """例子：
{"user_msg": "早上好", "current_name": "张三", "current_time": "2023-05-09 17:21:39"} 输出：张三你是不是睡糊涂了
{"user_msg": "下午好", "current_name": "李四", "current_time": "2022-11-39 16:34:15"} 输出：下午好呀李四
{"user_msg": "晚安", "current_name": "饭饭", "current_time": "2023-05-08 19:31:24"} 输出：才几点，不许睡！
{"user_msg": "晚安", "current_name": "饭饭", "current_time": "2023-05-08 21:31:24"} 输出：好健康的作息！饭饭明天见！
{"user_msg": "晚安", "current_name": "饭饭", "current_time": "2023-05-09 01:12:33"} 输出：哦，准备睡到明天中午吗？
"""

    max_tokens = 100
    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps({
                "user_msg": req,
                "current_name": get_name_by_event(event),
                "current_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            })}
        ],
        max_tokens=max_tokens,
        n=1,
        user=event_to_trace_id(event)
    )
    choice = completion['choices'][0]['message']['content']

    return choice
