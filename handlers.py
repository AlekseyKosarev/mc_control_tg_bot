from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
import kb
import admin_kb
import text
from auth import user_manager
import enums
from mc_server_manager import server_data
from wake_on_lan import wake_and_check
import callback_data
router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    user_id = msg.from_user.id
    user_name = msg.from_user.full_name
    user_manager.create_user(user_id, user_name, enums.UserRole.USER)
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.create_menu(user_id))

@router.message(F.text == "Меню")
async def menu(msg: Message):
    user_id = msg.from_user.id
    await msg.answer(text.menu, reply_markup=kb.create_menu(user_id))

@router.callback_query(F.data == callback_data.callback_main_menu)
async def menu(msg: Message):
    user_id = msg.from_user.id
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.create_menu(user_id))

@router.callback_query(F.data == callback_data.callback_player_count)
async def player_count_handler(callback: CallbackQuery):
    players = server_data["rcon_data"]["list"]["list_players"]
    
    if players:
        player_list = "\n".join(players)
        await callback.message.answer(f"Список игроков:\n{player_list}")
    else:
        await callback.message.answer("На сервере нет игроков.")

@router.callback_query(F.data == callback_data.callback_check_my_role)
async def role_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.answer(f"Ты {user_manager.get_user_role(user_id).value}")

@router.callback_query(F.data == callback_data.callback_start_server)
async def start_server_handler(callback: CallbackQuery):
    # Здесь вы можете добавить логику для запуска сервера
    # await callback.message.answer("Окей, запускаю сервер, подожди немного!")
    user_id = callback.from_user.id
    user_role = user_manager.get_user_role(user_id)
    if user_role == enums.UserRole.MODERATOR or user_role == enums.UserRole.ADMIN:
        await callback.message.answer("Пинаю сервер...")
        response = "Сервер оказался сильней... :( или нет, нажми /start"
        if wake_and_check():
            response = "Сервер успешно пробудился"
        await callback.message.answer(response)
    else:
        await callback.message.answer("Тебе не хватает прав!")

@router.callback_query(F.data == callback_data.callback_get_permission)  # Обработчик для кнопки "Стать модератором"
async def become_moderator_handler(callback: CallbackQuery):
    # Здесь вы можете добавить логику для изменения роли пользователя
    user_id = callback.from_user.id  # Получаем ID пользователя, который хочет стать модератором
    user_role = user_manager.get_user_role(user_id)  # Получаем роль пользователя

    # Проверяем, имеет ли пользователь уже роль модератора или администратора
    if user_role in [enums.UserRole.MODERATOR, enums.UserRole.ADMIN]:
        await callback.message.answer("У вас уже есть роль модератора или администратора.")
        return
    if user_role == enums.UserRole.PENDING_MODERATOR:
        await callback.message.answer("Да да, совсем скоро ты станешь большим модером(но это не точно)")
        return
    user_manager.change_user_role(user_id, enums.UserRole.PENDING_MODERATOR)
    await callback.message.answer("Запрос на модерацию отправлен администратору.")



@router.callback_query(F.data.startswith(callback_data.callback_accept_moderator))
async def confirm_moderator_handler(callback: CallbackQuery):
    user_id = callback.data.split(":")[1]  # Извлекаем ID пользователя из callback_data
    user_manager.change_user_role(user_id, enums.UserRole.MODERATOR)
    
    await callback.message.edit_text(f"Пользователь {user_id} теперь модератор.")

@router.callback_query(F.data.startswith(callback_data.callback_reject_moderator))
async def deny_moderator_handler(callback: CallbackQuery):
    user_id = callback.data.split(":")[1]
    user_manager.change_user_role(user_id, enums.UserRole.USER)
    await callback.message.edit_text(f"Запрос на модерацию пользователя {user_id} отклонен.")

@router.callback_query(F.data.startswith(callback_data.callback_delete_user))
async def deny_moderator_handler(callback: CallbackQuery):
    user_id = callback.data.split(":")[1]
    user_manager.delete_user(user_id)
    await callback.message.edit_text(f"Пользователь {user_id} удален.")

@router.callback_query(F.data == callback_data.callback_admin_action)
async def admin_settings(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_manager.get_user_by_id(user_id).has_role(enums.UserRole.ADMIN):
        await callback.message.edit_text(f"меню для выдачи прав модерации пользователям", reply_markup=admin_kb.main_admin_menu())

@router.callback_query(F.data == callback_data.callback_user_settings)
async def show_user_settings(callback: CallbackQuery):
    await callback.message.answer("Настройки юзер системы:", reply_markup=admin_kb.user_settings_menu())

@router.callback_query(F.data == callback_data.callback_file_settings)
async def show_file_settings(callback: CallbackQuery):
    await callback.message.answer("Настройки файловой системы:", reply_markup=admin_kb.file_settings_menu())

@router.callback_query(F.data == callback_data.callback_ssh_settings)
async def show_ssh_settings(callback: CallbackQuery):
    await callback.message.answer("Настройки SSH системы:", reply_markup=admin_kb.ssh_settings_menu())

@router.callback_query(F.data == callback_data.callback_select_players)
async def show_select_players(callback: CallbackQuery):
    await callback.message.answer("Выберите роль:", reply_markup=admin_kb.select_role_menu())

@router.callback_query(F.data.startswith(callback_data.callback_settings_role))
async def show_settings_role(callback: CallbackQuery):
    role_str = callback.data.split(":")[1]

    try:
        user_role = enums.UserRole.__getitem__(role_str)
        users = user_manager.get_users_by_role(user_role)
        await callback.message.answer(f"Все пользователи роли:{user_role}", reply_markup=admin_kb.settings_role_menu(users, user_role))
    except KeyError:
        users_all = user_manager.get_all_users()
        await callback.message.answer("Все пользователи:", reply_markup=admin_kb.settings_role_menu(users_all))