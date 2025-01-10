from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

import callback_data
from auth import User
from enums import UserRole


def main_admin_menu():
    menu = [
        [InlineKeyboardButton(text="Настройки юзер системы", callback_data=callback_data.callback_user_settings)],
        [InlineKeyboardButton(text="Настройки файловой системы", callback_data=callback_data.callback_file_settings)],
        [InlineKeyboardButton(text="Настройки SSH системы", callback_data=callback_data.callback_ssh_settings)],
        [InlineKeyboardButton(text="Назад", callback_data=callback_data.callback_main_menu)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=menu)


# Функция для меню настроек юзер системы
def user_settings_menu():
    menu = [
        [InlineKeyboardButton(text="Выбор списка игроков по ролям", callback_data=callback_data.callback_select_players)],
        [InlineKeyboardButton(text="Назад", callback_data=callback_data.callback_main_menu)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=menu)


# Функция для меню выбора списка игроков по ролям
def select_role_menu():
    menu = [[InlineKeyboardButton(text="Показать всех пользователей", callback_data=callback_data.callback_settings_role+"all")]]

    for role in UserRole:
        menu.append([InlineKeyboardButton(text=role.value.capitalize(), callback_data=callback_data.callback_settings_role+role.value)])

    menu.append([InlineKeyboardButton(text="Назад", callback_data=callback_data.callback_user_settings)])

    return InlineKeyboardMarkup(inline_keyboard=menu)


# Функция для меню настроек файловой системы
def file_settings_menu():
    menu = [
        [InlineKeyboardButton(text="Просмотреть содержимое файла", callback_data=callback_data.callback_list_file)],
        [InlineKeyboardButton(text="Удалить локальные файлы", callback_data=callback_data.callback_delete_local_files)],
        [InlineKeyboardButton(text="Назад", callback_data=callback_data.callback_main_menu)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=menu)


# Функция для меню настроек SSH системы
def ssh_settings_menu():
    menu = [
        [InlineKeyboardButton(text="Список файлов", callback_data=callback_data.callback_list_remote_files)],
        [InlineKeyboardButton(text="Удалить все удаленные файлы", callback_data=callback_data.callback_delete_remote_files)],
        [InlineKeyboardButton(text="Принудительное выключение сервера", callback_data=callback_data.callback_stop_server)],
        [InlineKeyboardButton(text="Назад", callback_data=callback_data.callback_main_menu)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=menu)


def settings_role_menu(users: list[User], only_role: UserRole = None):

    keyboard = [[InlineKeyboardButton(text="Назад", callback_data=callback_data.callback_user_settings)]]

    for user in users:
        if only_role is not None and user.role != only_role:
            continue
        user_name = user.nickname
        user_id = user.id
        combined_kb = [InlineKeyboardButton(text=user_name, callback_data=callback_data.callback_none)]

        if user.role is UserRole.PENDING_MODERATOR:
            combined_kb.append(InlineKeyboardButton(text="Принять", callback_data=callback_data.callback_accept_moderator+user_id))
            combined_kb.append(InlineKeyboardButton(text="Отклонить", callback_data=callback_data.callback_reject_moderator+user_id))
        combined_kb.append(InlineKeyboardButton(text="Удалить", callback_data=callback_data.callback_delete_user+user_id))
        keyboard.append(combined_kb)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
