# // EXTERNAL MODULES
import telebot


# REPLY KEYBOARDS
get_kb_reset_var = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).row("Скасувати")

get_kb_go_back_var = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).row("Назад")


def get_kb_main_menu():
    kb_main_menu = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    kb_main_menu.row("Інфо про мене")
    kb_main_menu.row("Налаштування")

    return kb_main_menu


def get_kb_gender_reset():
    kb_gender_reset = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    kb_gender_reset.row("Чоловіча")
    kb_gender_reset.row("Жіноча")
    kb_gender_reset.row("Скасувати")

    return kb_gender_reset


def get_kb_gender_go_back():
    kb_gender_go_back = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    kb_gender_go_back.row("Чоловіча")
    kb_gender_go_back.row("Жіноча")
    kb_gender_go_back.row("Назад")

    return kb_gender_go_back


def get_kb_settings():
    kb_settings = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    kb_settings.row("Змінити ім'я")
    kb_settings.row("Змінити вік")
    kb_settings.row("Змінити стать")
    kb_settings.row("Назад")

    return kb_settings
