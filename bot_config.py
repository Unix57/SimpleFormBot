import os


TGM_BOT_TOKEN_DEFAULT_1 = "2059333738:AAHArjXlbrcmu-1K2d4fzDF3WmLorWgPzXs"

TGM_BOT_TOKEN_1 = os.getenv("TGM_BOT_TOKEN")

if TGM_BOT_TOKEN_1 is None:
    os.environ["TGM_BOT_TOKEN"] = TGM_BOT_TOKEN_DEFAULT_1
    TGM_BOT_TOKEN_1 = os.getenv("TGM_BOT_TOKEN")

HEROKU_APP_NAME_1 = os.getenv("HEROKU_APP_NAME")

if HEROKU_APP_NAME_1 is None:
    os.environ["HEROKU_APP_NAME"] = "simple-form-bot-v1"
    HEROKU_APP_NAME_1 = os.getenv("HEROKU_APP_NAME")
