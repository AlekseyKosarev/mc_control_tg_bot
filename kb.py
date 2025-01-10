from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from auth import user_manager
from mc_server_manager import server_data
from enums import UserRole
import callback_data
# Пример статуса сервера и количества игроков
# server_online = "🟢"  # Зелёный круг для онлайн

# Функция для создания меню
def create_menu(user_id):
    # Определяем статус сервера
    server_online = "🟢" if server_data["online"] else "🔴"  # Зеленый круг для онлайн, красный для оффлайн
    current_players = server_data["rcon_data"]["list"]["current_players"]
    max_players = server_data["rcon_data"]["list"]["max_players"]

    # Создание меню
    menu = [
        [InlineKeyboardButton(text=f"Статус сервера: {server_online}", callback_data=callback_data.callback_server_status)],
        [InlineKeyboardButton(text=f"👥 Количество игроков: {current_players}/{max_players}", callback_data=callback_data.callback_player_count)],
        [InlineKeyboardButton(text="👥 Твоя роль", callback_data=callback_data.callback_check_my_role)],
        [InlineKeyboardButton(text="🔌 Включить сервер", callback_data=callback_data.callback_start_server)],
        [InlineKeyboardButton(text="Стать модератором", callback_data=callback_data.callback_get_permission)]
    ]
    # Проверяем, является ли пользователь администратором
    if user_manager.get_user_by_id(user_id).has_role(UserRole.ADMIN):
        print("ты есть админ")
        menu.append([InlineKeyboardButton(text="🔧 Админская менюшка", callback_data=callback_data.callback_admin_action)])

    return InlineKeyboardMarkup(inline_keyboard=menu)

def empty_kb():
    empty_keyboard = InlineKeyboardButton(text="Запрос подтвержден", callback_data=callback_data.callback_none)
    return InlineKeyboardMarkup(inline_keyboard=empty_keyboard)

