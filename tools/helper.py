import time
import hashlib
from typing import Union

from mirai import FriendMessage, GroupMessage
from redis import Redis

redis = Redis()
name_key_prefix = "user_name"


def event_to_system(event: Union[FriendMessage, GroupMessage]):
    context = ""

    if isinstance(event, FriendMessage):
        context += f"以下消息发自好友{event.sender.get_name()}，消息来自私聊。"
    elif isinstance(event, GroupMessage):
        context += f"以下消息发自群{event.sender.group.get_name()}中的群名片是{event.sender.get_name()}的用户。"

    context += f"系统中您对他的称呼是{get_name_by_event(event)}。"

    return context


def event_to_trace_id(event: Union[FriendMessage, GroupMessage]):
    prefix = "gpbt"
    trace_id = hashlib.sha3_256(f"{prefix}-{str(event.sender.id)}".encode())
    return trace_id.hexdigest()


def set_name_by_event(name: str, event: Union[FriendMessage, GroupMessage]):
    redis.set(f"{name_key_prefix}:{event.sender.id}", name)


def get_name_by_event(event: Union[FriendMessage, GroupMessage]):
    name = redis.get(f"{name_key_prefix}:{event.sender.id}")
    if name is None:
        name = event.sender.get_name()
        set_name_by_event(name, event)
        return name
    return name.decode()


def current_time_to_system():
    return time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime())
