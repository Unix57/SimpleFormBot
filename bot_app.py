# BUILT-IN MODULES
import os
import logging

# EXTERNAL MODULES
import telebot
from flask import Flask, request
from flask_sslify import SSLify

# LOCAL MODULES
import bot_sqlite_db_ops as local_db
import bot_keyboards as keyboards
import bot_config as config

# ENVIRONMENTAL VARIABLES
TGM_BOT_TOKEN_DEFAULT = config.TGM_BOT_TOKEN_DEFAULT_1  # @simpleform4_bot

TGM_BOT_TOKEN = config.TGM_BOT_TOKEN_DEFAULT_1

HEROKU_APP_NAME = config.HEROKU_APP_NAME_1

# TELEGRAM-BOT
bot = telebot.TeleBot(TGM_BOT_TOKEN)

bot.enable_save_next_step_handlers(delay=0, filename="./.handlers-saves/step.save")
bot.load_next_step_handlers(filename="./.handlers-saves/step.save")

# FLASK-APP
flask_app = Flask(__name__)
ssl_flask_app = SSLify(flask_app)

# LOGGER CONFIG
logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.DEBUG)

# DATABASE TABLES/COLUMNS DICTS
db_tables = local_db.db_tables_dict
user_data_cols = local_db.user_data_cols_dict

# DATABASE CONFIG
db_conn_name = "bot_local_sqlite3.db"

if __name__ == "__main__":
    if os.path.exists(db_conn_name):
        logging.debug(f"--- DATABASE | {db_conn_name} | EXISTS --- NO ESTABLISHMENT NEEDED ---")
    else:
        local_db.init_database(db_conn_name)
        logging.debug(f"--- DB FILE CREATED --- DATABASE | {db_conn_name} | ESTABLISHED ---")


# REPLY KEYBOARDS
kb_reset = keyboards.kb_reset_val
kb_go_back = keyboards.kb_go_back_val

kb_main_menu = keyboards.kb_main_menu_func()
kb_settings = keyboards.kb_settings_func()
kb_gender_reset = keyboards.kb_gender_reset_func()
kb_gender_go_back = keyboards.kb_gender_go_back_func()

# VARS
user_states_dict = {
    "state_default": "state_default",
    "state_settings_menu": "state_settings_menu"
}


@bot.message_handler(commands=["start"])
def start_msg(message):
    user_reg_flag = local_db.UserDataCRUD.check_user_reg_flag(db_conn_name, message.chat.id)

    if not user_reg_flag[0]:
        local_db.UserDataCRUD.add_new_user(db_conn_name, message.chat.id)
        bot.send_message(message.chat.id,
                         "Вітаю у @simpleform4_bot.\n"
                         "Для початку анкетування будь ласка введіть Ваше ім'я:",
                         reply_markup=kb_reset)
    else:
        bot.send_message(message.chat.id,
                         "Повторне анкетування.\n"
                         "Будь ласка введіть Ваше ім'я:",
                         reply_markup=kb_reset)

    bot.register_next_step_handler(message, UserPolling.get_user_name)
    bot.next_step


class UserPolling(object):
    @staticmethod
    def get_user_name(message):
        name_message = message.text

        if message.text == "Скасувати":
            UserPolling.cancel_user_polling(message)

        elif 1 < len(name_message) < 21 and not name_message.startswith("/"):
            user_name = message.text
            local_db.UserDataCRUD.upd_user_col(db_conn_name, user_data_cols["name"], user_name, message.chat.id)

            bot.send_message(message.chat.id, f"Ваше ім'я: {user_name}")
            bot.send_message(message.chat.id, "Введіть Ваш вік (повних років):", reply_markup=kb_reset)

            bot.register_next_step_handler(message, UserPolling.get_user_age)

        else:
            bot.send_message(message.chat.id,
                             "Некоректний формат вводу.\n"
                             "Ім'я має містити від 2 до 20 символів.\n\n"
                             "Повторіть спробу.",
                             reply_markup=kb_reset)
            bot.register_next_step_handler(message, UserPolling.get_user_name)

    @staticmethod
    def get_user_age(message):
        age_message = message.text

        if age_message.isdigit() and 1 < int(age_message) < 103:
            user_age = age_message
            local_db.UserDataCRUD.upd_user_col(db_conn_name, user_data_cols["age"], user_age, message.chat.id)

            bot.send_message(message.chat.id, f"Ваш вік: {user_age}")
            bot.send_message(message.chat.id, "Оберіть Вашу стать:", reply_markup=kb_gender_reset)

            bot.register_next_step_handler(message, UserPolling.get_user_gender)

        elif message.text == "Скасувати":
            UserPolling.cancel_user_polling(message)

        else:
            bot.send_message(message.chat.id,
                             "Некоректний формат вводу.\n"
                             "Вік має бути цілим числом від 2 до 102 включно.\n\n"
                             "Повторіть спробу.",
                             reply_markup=kb_reset)
            bot.register_next_step_handler(message, UserPolling.get_user_age)

    @staticmethod
    def get_user_gender(message):
        gender_message = message.text

        if gender_message == "Чоловіча" or gender_message == "Жіноча":
            user_gender = gender_message
            local_db.UserDataCRUD.upd_user_col(db_conn_name, user_data_cols["gender"], user_gender, message.chat.id)

            bot.send_message(message.chat.id, f"Ваша стать: {user_gender}")

            user_reg_flag = local_db.UserDataCRUD.check_user_reg_flag(db_conn_name, message.chat.id)

            if not user_reg_flag:
                local_db.UserDataCRUD.upd_user_reg_flag(db_conn_name, 1, message.chat.id)

            bot.send_message(message.chat.id,
                             "Ваші дані збережено.\n\n"
                             "Для перегляду особистих даних оберіть пункт «Інфо про мене» у /menu.\n\n"
                             "Для зміни особистих данихперейдіть у розділ «Налаштування» у /menu.",
                             reply_markup=kb_main_menu)

        elif message.text == "Скасувати":
            UserPolling.cancel_user_polling(message)

        else:
            bot.send_message(message.chat.id,
                             "Некоректний формат вводу.\n\n"
                             "Повторіть спробу.",
                             reply_markup=kb_gender_reset)
            bot.register_next_step_handler(message, UserPolling.get_user_gender)

    @staticmethod
    def cancel_user_polling(message):
        bot.send_message(message.chat.id, "Введення даних скасовано.\n"
                                          "Натисніть /start для початку анкетування.")
        # bot.register_next_step_handler(message, start_msg)


@bot.message_handler(commands=["menu"])
def menu_msg(message):
    local_db.UserDataCRUD.upd_user_state(db_conn_name, user_states_dict["state_default"], message.chat.id)
    user_reg_flag = local_db.UserDataCRUD.check_user_reg_flag(db_conn_name, message.chat.id)

    if user_reg_flag:
        bot.send_message(message.chat.id, "/menu\nГоловне меню:", reply_markup=kb_main_menu)

    else:
        bot.send_message(message.chat.id,
                         "Функція меню доступна лише зареєстрованим користувачам.\n"
                         "Для реєстрації пройдіть коротке анкетування.\n\n"
                         "Пройти анкетування можна за командою /start.")


# func=lambda message: True,
@bot.message_handler(func=lambda message: True, content_types=["text"])
def handler_text(message):
    user_reg_flag = local_db.UserDataCRUD.check_user_reg_flag(db_conn_name, message.chat.id)
    logging.warning(f"--- USER_REG_FLAG --- {user_reg_flag=}")

    if user_reg_flag:
        user_state_check = local_db.UserDataCRUD.get_user_state(db_conn_name, message.chat.id)

        if user_state_check[0] == user_states_dict["state_default"]:
            if message.text == "Інфо про мене":
                MainMenu.send_user_info_msg(message)

            elif message.text == "Налаштування":
                local_db.UserDataCRUD.upd_user_state(db_conn_name, user_states_dict["state_settings_menu"],
                                                     message.chat.id)

                bot.send_message(message.chat.id, "Налаштування:", reply_markup=kb_settings)

            else:
                bot.send_message(message.chat.id, "Команда відсутня")

        elif user_state_check[0] == user_states_dict["state_settings_menu"]:
            if message.text == "Змінити ім'я":
                bot.send_message(message.chat.id, "Введіть Ваше нове ім'я:", reply_markup=kb_go_back)

                bot.register_next_step_handler(message, SettingsMenu.change_user_name)

            elif message.text == "Змінити вік":
                bot.send_message(message.chat.id, "Введіть Ваш новий вік:", reply_markup=kb_go_back)

                bot.register_next_step_handler(message, SettingsMenu.change_user_age)

            elif message.text == "Змінити стать":
                bot.send_message(message.chat.id, "Оберіть Вашу нову стать:", reply_markup=kb_gender_go_back)

                bot.register_next_step_handler(message, SettingsMenu.change_user_gender)

            elif message.text == "Назад":
                local_db.UserDataCRUD.upd_user_state(db_conn_name, user_states_dict["state_default"], message.chat.id)

                bot.send_message(message.chat.id, "/menu\nГоловне меню:", reply_markup=kb_main_menu)

                bot.register_next_step_handler(message, handler_text)

            else:
                bot.send_message(message.chat.id, "Команда відсутня")

    else:
        bot.send_message(message.chat.id,
                         "Ви не зареєстровані у системі.\n"
                         "Для реєстрації пройдіть коротке анкетування.\n\n"
                         "Пройти анкетування можна за командою /start.")


class MainMenu:
    @staticmethod
    def send_user_info_msg(message):
        user_data_tup = local_db.UserDataCRUD.read_user_data(db_conn_name, message.chat.id)

        if user_data_tup:
            user_name, user_age, user_gender = user_data_tup

            bot.send_message(message.chat.id,
                             f"Інфо користувача @{message.chat.username}:\n"
                             f"Ім'я: {user_name}\n"
                             f"Вік: {user_age}\n"
                             f"Стать: {user_gender}")

            bot.send_message(message.chat.id, "/menu\nГоловне меню:", reply_markup=kb_main_menu)


class SettingsMenu:
    @staticmethod
    def change_user_name(message):
        name_message = message.text

        if message.text == "Назад":
            bot.send_message(message.chat.id, "Зміна імені скасована", reply_markup=kb_settings)

            bot.register_next_step_handler(message, handler_text)

        elif 1 < len(name_message) < 21 and not name_message.startswith("/"):
            user_name = name_message
            local_db.UserDataCRUD.upd_user_col(db_conn_name, user_data_cols["name"], user_name, message.chat.id)
            bot.send_message(message.chat.id, f"Ваше нове ім'я: {user_name}", reply_markup=kb_settings)

        else:
            bot.send_message(message.chat.id,
                             "Некоректний формат вводу.\n"
                             "Ім'я має містити від 2 до 20 символів включно.\n"
                             "Повторіть спробу.",
                             reply_markup=kb_go_back)

            bot.register_next_step_handler(message, SettingsMenu.change_user_name)

    @staticmethod
    def change_user_age(message):
        age_message = message.text

        if age_message.isdigit() and 1 < int(age_message) < 103:
            user_age = age_message
            local_db.UserDataCRUD.upd_user_col(db_conn_name, user_data_cols["age"], user_age, message.chat.id)
            bot.send_message(message.chat.id, f"Ваш оновлений вік: {user_age}", reply_markup=kb_settings)

        elif message.text == "Назад":
            bot.send_message(message.chat.id, "Зміна віку скасована", reply_markup=kb_settings)

            bot.register_next_step_handler(message, handler_text)

        else:
            bot.send_message(message.chat.id,
                             "Некоректний формат вводу.\n"
                             "Вік має бути цілим числом від 2 до 102 включно.\n"
                             "Повторіть спробу.",
                             reply_markup=kb_go_back)

            bot.register_next_step_handler(message, SettingsMenu.change_user_age)

    @staticmethod
    def change_user_gender(message):
        gender_message = message.text

        if gender_message == "Чоловіча" or gender_message == "Жіноча":
            user_gender = gender_message
            local_db.UserDataCRUD.upd_user_col(db_conn_name, user_data_cols["gender"], user_gender, message.chat.id)
            bot.send_message(message.chat.id, f"Ваша нова стать: {user_gender}", reply_markup=kb_settings)

        elif message.text == "Назад":
            bot.send_message(message.chat.id, "Зміна статі скасована", reply_markup=kb_settings)

            bot.register_next_step_handler(message, handler_text)

        else:
            bot.send_message(message.chat.id,
                             "Некоректний формат вводу.\n"
                             "Повторіть спробу.",
                             reply_markup=kb_gender_go_back)

            bot.register_next_step_handler(message, SettingsMenu.change_user_gender)


# set_webhook_url_test_1 = "https://9c55-31-40-108-124.ngrok.io/2090254399:AAGn_Njw75I9szKUmPKN-T37_F3Y12hAf18/"
# set_webhook_url_heroku_1 = "https://simple-form-bot-v1.herokuapp.com/2090254399:AAGn_Njw75I9szKUmPKN-T37_F3Y12hAf18/"

flask_app_url = f"https://{HEROKU_APP_NAME}.herokuapp.com/"
bot_webhook_info_url = f"https://api.telegram.org/bot{TGM_BOT_TOKEN}/getWebhookInfo"

set_webhook_url_test = f"https://9c55-31-40-108-124.ngrok.io/{TGM_BOT_TOKEN}/"
set_webhook_url_heroku = f"https://{HEROKU_APP_NAME}.herokuapp.com/{TGM_BOT_TOKEN}/"


if "HEROKU_DEPLOY" in list(os.environ.keys()):
    logging.debug("--- HEROKU_DEPLOY --- TRUE ---")

    @flask_app.route("/reset", methods=["GET"])
    def webhook():
        bot.remove_webhook()
        logging.debug("--- HEROKU_DEPLOY --- WEBHOOK --- REMOVE-WEBHOOK ---")

        bot.set_webhook(set_webhook_url_heroku)
        logging.debug("--- HEROKU_DEPLOY --- WEBHOOK --- SET-WEBHOOK ---")

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
