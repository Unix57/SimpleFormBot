import os


TGM_BOT_TOKEN_DEFAULT_1 = "2090254399:AAGn_Njw75I9szKUmPKN-T37_F3Y12hAf18"

os.environ["TGM_BOT_TOKEN"] = TGM_BOT_TOKEN_DEFAULT_1
TGM_BOT_TOKEN_1 = os.getenv("TGM_BOT_TOKEN")

if TGM_BOT_TOKEN_1 is None:
    os.environ["TGM_BOT_TOKEN"] = TGM_BOT_TOKEN_DEFAULT_1
    TGM_BOT_TOKEN_1 = os.getenv("TGM_BOT_TOKEN")

os.environ["HEROKU_APP_NAME"] = "simple-form-bot-v1"
HEROKU_APP_NAME_1 = os.getenv("HEROKU_APP_NAME")
