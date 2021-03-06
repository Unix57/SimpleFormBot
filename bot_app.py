# // BUILT-IN MODULES
import os
import logging

# // EXTERNAL MODULES
import telebot
from flask import Flask, request
from flask_sslify import SSLify

# // LOCAL MODULES
import bot_sqlite_db_ops as local_db
from bot_sqlite_db_ops import UserDataCRUD
import bot_keyboards as keyboards
import bot_config as config

# |---| ENVIRONMENTAL VARIABLES
TGM_BOT_TOKEN_DEFAULT = config.TGM_BOT_TOKEN_DEFAULT_config  # @simpleform4_bot

TGM_BOT_TOKEN = config.TGM_BOT_TOKEN_env

HEROKU_APP_NAME = config.HEROKU_APP_NAME_env

# |---| TELEGRAM-BOT
bot = telebot.TeleBot(TGM_BOT_TOKEN)

# |---| FLASK-APP
flask_app = Flask(__name__)
ssl_flask_app = SSLify(flask_app)

# |---| DEBUG LOGGER CONFIG
logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.DEBUG)

# |---| DATABASE TABLES/COLUMNS DICTS
db_tables = local_db.db_tables_dict
user_data_cols = local_db.user_data_cols_dict

# |---| DATABASE CONFIG
db_conn_name = config.DB_CONN_NAME_env

if __name__ == "__main__":
    if os.path.exists(db_conn_name):
        logging.info(f"--- DATABASE | {db_conn_name} | --- EXISTS ---")
    else:
        logging.warning(f"--- DATABASE | {db_conn_name} | --- NOT FOUND---")

        local_db.init_database(db_conn_name)

        logging.warning(f"--- DATABASE | {db_conn_name} | --- INITIALIZED ---")

# |---| REPLY KEYBOARDS
hide_kb = telebot.types.ReplyKeyboardRemove()

kb_reset = keyboards.get_kb_reset_var
kb_go_back = keyboards.get_kb_go_back_var

kb_main_menu = keyboards.get_kb_main_menu()
kb_settings = keyboards.get_kb_settings()
kb_gender_reset = keyboards.get_kb_gender_reset()
kb_gender_go_back = keyboards.get_kb_gender_go_back()

# |---| USER STATE DICTS
user_states = {
    "user_polling": "user_polling",
    "state_default": "state_default",
    "settings_menu": "settings_menu"
}

user_polling_states = {
    "input_name": "user_polling/input_name",
    "input_age": "user_polling/input_age",
    "input_gender": "user_polling/input_gender"
}

settings_menu_states = {
    "edit_name": "settings_menu/edit_name",
    "edit_age": "settings_menu/edit_age",
    "edit_gender": "settings_menu/edit_gender"
}


@bot.message_handler(commands=["start"])
def start_msg(message):
    user_reg_flag = UserDataCRUD.check_user_reg_flag(db_conn_name, message.chat.id)
    user_check = UserDataCRUD.check_user_cid(db_conn_name, message.chat.id)

    if not user_check:
        UserDataCRUD.add_new_user(db_conn_name, message.chat.id)

    if user_reg_flag:
        bot.send_message(message.chat.id,
                         "???????????????? ??????????????????????.\n"
                         "???????? ?????????? ?????????????? ???????? ????'??:",
                         reply_markup=kb_reset)
    else:
        bot.send_message(message.chat.id,
                         "?????????? ?? @simpleform4_bot.\n"
                         "?????? ?????????????? ?????????????????????? ???????? ?????????? ?????????????? ???????? ????'??:",
                         reply_markup=kb_reset)

    UserDataCRUD.upd_user_state(db_conn_name, user_polling_states["input_name"], message.chat.id)


@bot.message_handler(commands=["menu"])
def menu_msg(message):
    UserDataCRUD.upd_user_state(db_conn_name, user_states["state_default"], message.chat.id)

    user_reg_flag = UserDataCRUD.check_user_reg_flag(db_conn_name, message.chat.id)

    if user_reg_flag:
        bot.send_message(message.chat.id, "/menu\n?????????????? ????????:", reply_markup=kb_main_menu)

    else:
        bot.send_message(message.chat.id,
                         "- ?????????????? ???????? ???????????????? ???????? ???????????????????????????? ????????????????????????.\n"
                         "- ?????? ???????????????????? ???????????????? ?????????????? ??????????????????????.\n\n"
                         "?????????????????? /start ?????? ?????????????? ??????????????????????")


@bot.message_handler(func=lambda message: True, content_types=["text"])
def handler_text(message):
    user_check = UserDataCRUD.check_user_cid(db_conn_name, message.chat.id)

    if user_check:
        user_reg_flag = UserDataCRUD.check_user_reg_flag(db_conn_name, message.chat.id)
        logging.warning(f"--- USER_REG_FLAG --- {user_reg_flag=}")

        user_state = UserDataCRUD.get_user_state(db_conn_name, message.chat.id)

        if user_state[0].startswith(user_states["user_polling"]):  # UserPolling Steps
            if user_polling_states["input_name"] in user_state[0]:
                UserPolling.get_user_name(message)

            elif user_polling_states["input_age"] in user_state[0]:
                UserPolling.get_user_age(message)

            elif user_polling_states["input_gender"] in user_state[0]:
                UserPolling.get_user_gender(message)

        elif user_state[0].startswith(user_states["settings_menu"]):  # SettingsMenu Options
            if settings_menu_states["edit_name"] in user_state[0]:
                SettingsMenu.edit_user_name(message)

            elif settings_menu_states["edit_age"] in user_state[0]:
                SettingsMenu.edit_user_age(message)

            elif settings_menu_states["edit_gender"] in user_state[0]:
                SettingsMenu.edit_user_gender(message)

        if user_reg_flag:
            if user_state[0] == user_states["state_default"]:
                if message.text == "???????? ?????? ????????":
                    MainMenu.send_user_info_msg(message)

                elif message.text == "????????????????????????":
                    UserDataCRUD.upd_user_state(db_conn_name, user_states["settings_menu"], message.chat.id)

                    bot.send_message(message.chat.id, "????????????????????????:", reply_markup=kb_settings)

                else:
                    bot.send_message(message.chat.id, "?????????????? ????????????????")

            elif user_state[0] == user_states["settings_menu"]:
                if message.text == "?????????????? ????'??":
                    bot.send_message(message.chat.id, "?????????????? ???????? ???????? ????'??:", reply_markup=kb_go_back)

                    UserDataCRUD.upd_user_state(db_conn_name, settings_menu_states["edit_name"], message.chat.id)

                elif message.text == "?????????????? ??????":
                    bot.send_message(message.chat.id, "?????????????? ?????? ?????????? ??????:", reply_markup=kb_go_back)

                    UserDataCRUD.upd_user_state(db_conn_name, settings_menu_states["edit_age"], message.chat.id)

                elif message.text == "?????????????? ??????????":
                    bot.send_message(message.chat.id, "?????????????? ???????? ???????? ??????????:", reply_markup=kb_gender_go_back)

                    UserDataCRUD.upd_user_state(db_conn_name, settings_menu_states["edit_gender"], message.chat.id)

                elif message.text == "??????????":
                    UserDataCRUD.upd_user_state(db_conn_name, user_states["state_default"], message.chat.id)

                    bot.send_message(message.chat.id, "/menu\n?????????????? ????????:", reply_markup=kb_main_menu)

                else:
                    bot.send_message(message.chat.id, "?????????????? ????????????????")

        else:
            if user_state[0] == user_states["state_default"] and not user_reg_flag:
                bot.send_message(message.chat.id,
                                 "- ???? ???? ?????????????????????????? ?? ??????????????.\n"
                                 "- ?????? ???????????????????? ???????????????? ?????????????? ??????????????????????.\n\n"
                                 "?????????????????? /start ?????? ?????????????? ??????????????????????",
                                 reply_markup=hide_kb)

    else:
        bot.send_message(message.chat.id,
                         "?????? ???????????????????? ?????????????????????????? ?????????????????? ?? ??????????????.\n"
                         "?????????????????? /start ?????? ?????????????? ??????????????????????",
                         reply_markup=hide_kb)


class UserPolling:
    @staticmethod
    def get_user_name(message):
        name_message = message.text

        if message.text == "??????????????????":
            UserPolling.cancel_user_polling(message)

        elif 1 < len(name_message) < 21 and not name_message.startswith("/"):
            user_name = message.text
            UserDataCRUD.upd_user_col(db_conn_name, user_data_cols["name"], user_name, message.chat.id)

            bot.send_message(message.chat.id, f"???????? ????'??: {user_name}")

            UserDataCRUD.upd_user_state(db_conn_name, user_polling_states["input_age"], message.chat.id)

            bot.send_message(message.chat.id, "?????????????? ?????? ?????? (???????????? ??????????):", reply_markup=kb_reset)

        else:
            bot.send_message(message.chat.id,
                             "- ?????????????????????? ???????????? ??????????.\n"
                             "- ????'?? ?????? ?????????????? ?????? 2 ???? 20 ????????????????.\n"
                             "?????????????????? ????????????.",
                             reply_markup=kb_reset)

    @staticmethod
    def get_user_age(message):
        age_message = message.text

        if age_message.isdigit() and 1 < int(age_message) < 103:
            user_age = age_message
            UserDataCRUD.upd_user_col(db_conn_name, user_data_cols["age"], user_age, message.chat.id)

            bot.send_message(message.chat.id, f"?????? ??????: {user_age}")

            UserDataCRUD.upd_user_state(db_conn_name, user_polling_states["input_gender"], message.chat.id)

            bot.send_message(message.chat.id, "?????????????? ???????? ??????????:", reply_markup=kb_gender_reset)

        elif message.text == "??????????????????":
            UserPolling.cancel_user_polling(message)

        else:
            bot.send_message(message.chat.id,
                             "- ?????????????????????? ???????????? ??????????.\n"
                             "- ?????? ?????? ???????? ?????????? ???????????? ?????? 2 ???? 102 ??????????????.\n"
                             "?????????????????? ????????????.",
                             reply_markup=kb_reset)

    @staticmethod
    def get_user_gender(message):
        gender_message = message.text

        if gender_message == "????????????????" or gender_message == "????????????":
            user_gender = gender_message
            UserDataCRUD.upd_user_col(db_conn_name, user_data_cols["gender"], user_gender, message.chat.id)

            bot.send_message(message.chat.id, f"???????? ??????????: {user_gender}")

            user_reg_flag = UserDataCRUD.check_user_reg_flag(db_conn_name, message.chat.id)

            if not user_reg_flag:
                UserDataCRUD.upd_user_reg_flag(db_conn_name, 1, message.chat.id)

            UserDataCRUD.upd_user_state(db_conn_name, user_states["state_default"], message.chat.id)

            bot.send_message(message.chat.id,
                             "???????? ???????????????? ???????? ??????????????????.\n\n"
                             "- ?????? ?????????????????? ?????????????????? ?????????? ?????????????? ?????????? ?????????? ?????? ?????????? /menu.\n"
                             "- ?????????? ?????????????????? ?????????? ???????????????? ?? ?????????????? ???????????????????????????? /menu.",
                             reply_markup=kb_main_menu)

        elif message.text == "??????????????????":
            UserPolling.cancel_user_polling(message)

        else:
            bot.send_message(message.chat.id,
                             "- ?????????????????????? ???????????? ??????????.\n"
                             "?????????????????? ????????????.",
                             reply_markup=kb_gender_reset)

    @staticmethod
    def cancel_user_polling(message):
        UserDataCRUD.upd_user_state(db_conn_name, user_states["state_default"], message.chat.id)

        bot.send_message(message.chat.id, "???????????????? ?????????? ??????????????????.\n"
                                          "?????????????????? /start ?????? ?????????????? ??????????????????????")


class MainMenu:
    @staticmethod
    def send_user_info_msg(message):
        user_data_tup = UserDataCRUD.read_user_data(db_conn_name, message.chat.id)

        if user_data_tup:
            user_name, user_age, user_gender = user_data_tup

            bot.send_message(message.chat.id,
                             f"???????? ?????????????????????? @{message.chat.username}:\n"
                             f"- ????'??: {user_name}\n"
                             f"- ??????: {user_age}\n"
                             f"- ??????????: {user_gender}")

            bot.send_message(message.chat.id, "/menu\n?????????????? ????????:", reply_markup=kb_main_menu)


class SettingsMenu:
    @staticmethod
    def edit_user_name(message):
        name_message = message.text

        if message.text == "??????????":
            bot.send_message(message.chat.id, "?????????? ?????????? ??????????????????", reply_markup=kb_settings)

            UserDataCRUD.upd_user_state(db_conn_name, user_states["settings_menu"], message.chat.id)

        elif 1 < len(name_message) < 21 and not name_message.startswith("/"):
            user_name = name_message
            UserDataCRUD.upd_user_col(db_conn_name, user_data_cols["name"], user_name, message.chat.id)

            bot.send_message(message.chat.id, f"???????? ???????? ????'??: {user_name}", reply_markup=kb_settings)

            UserDataCRUD.upd_user_state(db_conn_name, user_states["settings_menu"], message.chat.id)

        else:
            bot.send_message(message.chat.id,
                             "- ?????????????????????? ???????????? ??????????.\n"
                             "- ????'?? ?????? ?????????????? ?????? 2 ???? 20 ???????????????? ??????????????.\n"
                             "?????????????????? ????????????.",
                             reply_markup=kb_go_back)

    @staticmethod
    def edit_user_age(message):
        age_message = message.text

        if age_message.isdigit() and 1 < int(age_message) < 103:
            user_age = age_message
            UserDataCRUD.upd_user_col(db_conn_name, user_data_cols["age"], user_age, message.chat.id)

            bot.send_message(message.chat.id, f"?????? ?????????????????? ??????: {user_age}", reply_markup=kb_settings)

            UserDataCRUD.upd_user_state(db_conn_name, user_states["settings_menu"], message.chat.id)

        elif message.text == "??????????":
            bot.send_message(message.chat.id, "?????????? ???????? ??????????????????", reply_markup=kb_settings)

            UserDataCRUD.upd_user_state(db_conn_name, user_states["settings_menu"], message.chat.id)

        else:
            bot.send_message(message.chat.id,
                             "- ?????????????????????? ???????????? ??????????.\n"
                             "- ?????? ?????? ???????? ?????????? ???????????? ?????? 2 ???? 102 ??????????????.\n"
                             "?????????????????? ????????????.",
                             reply_markup=kb_go_back)

    @staticmethod
    def edit_user_gender(message):
        gender_message = message.text

        if gender_message == "????????????????" or gender_message == "????????????":
            user_gender = gender_message
            UserDataCRUD.upd_user_col(db_conn_name, user_data_cols["gender"], user_gender, message.chat.id)

            bot.send_message(message.chat.id, f"???????? ???????? ??????????: {user_gender}", reply_markup=kb_settings)

            UserDataCRUD.upd_user_state(db_conn_name, user_states["settings_menu"], message.chat.id)

        elif message.text == "??????????":
            bot.send_message(message.chat.id, "?????????? ?????????? ??????????????????", reply_markup=kb_settings)

            UserDataCRUD.upd_user_state(db_conn_name, user_states["settings_menu"], message.chat.id)

        else:
            bot.send_message(message.chat.id,
                             "- ?????????????????????? ???????????? ??????????.\n"
                             "?????????????????? ????????????.",
                             reply_markup=kb_gender_go_back)


if "HEROKU_DEPLOY" in list(os.environ.keys()):
    logging.info("--- HEROKU_DEPLOY --- TRUE ---")

    @flask_app.route("/reset", methods=["GET"])
    def webhook():
        set_webhook_url_heroku = f"https://{HEROKU_APP_NAME}.herokuapp.com/{TGM_BOT_TOKEN}/"

        bot.remove_webhook()
        logging.info("--- HEROKU_DEPLOY --- WEBHOOK --- REMOVE-WEBHOOK ---")

        bot.set_webhook(set_webhook_url_heroku)
        logging.info("--- HEROKU_DEPLOY --- WEBHOOK --- SET-WEBHOOK ---")

        return "FLASK-APP SET-WEBHOOK ROUTE", 200

    @flask_app.route(f"/{TGM_BOT_TOKEN}/", methods=["POST"])
    def get_message():
        json_str = request.stream.read().decode("utf-8")
        bot.process_new_updates([telebot.types.Update.de_json(json_str)])

        return "FLASK-APP TGM-BOT ROUTE", 200

else:
    logging.critical("--- HEROKU_DEPLOY --- NOT FOUND ---")

# --- HEROKU-DEPLOY PROCFILE ---
# Procfile PROD - web: gunicorn --bind 0.0.0.0:$PORT bot_app:flask_app
# Procfile TEST - web: python bot_app.py runserver 0.0.0.0:$PORT

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8443))
    flask_app.run(host="0.0.0.0", port=port, threaded=True, debug=True)
