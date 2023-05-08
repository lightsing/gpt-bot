import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

if OPENAI_API_KEY is None:
    OPENAI_API_KEY = "SUPER SECRET KEY"

BOT_ID = os.environ.get("QQ_BOT_ID")

if BOT_ID is None:
    BOT_ID = 123456

ADAPTER = None
