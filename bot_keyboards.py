# EXTERNAL MODULES
import telebot


# REPLY MARKUP KEYBOARDS
kb_reset_val = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).row("Скасувати")

kb_go_back_val = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).row("Назад")


def kb_main_menu_func():
    kb_main_menu = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    kb_main_menu.row("Інфо про мене")
    kb_main_menu.row("Налаштування")

    return kb_main_menu


def kb_gender_reset_func():
    kb_gender_reset = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    kb_gender_reset.row("Чоловіча")
    kb_gender_reset.row("Жіноча")
    kb_gender_reset.row("Скасувати")

    return kb_gender_reset


def kb_gender_go_back_func():
    kb_gender_go_back = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    kb_gender_go_back.row("Чоловіча")
    kb_gender_go_back.row("Жіноча")
    kb_gender_go_back.row("Назад")

    return kb_gender_go_back


def kb_settings_func():
    kb_settings = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    kb_settings.row("Змінити ім'я")
    kb_settings.row("Змінити вік")
    kb_settings.row("Змінити стать")
    kb_settings.row("Назад")

    return kb_settings
