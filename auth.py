import json
import asyncio
from enums import UserRole, FileNamesEnum
from config import SAVE_INTERVAL
from json_file_manager import load, save
from typing import Union, List, Callable, Dict
from decorators import singleton
lock = asyncio.Lock()


class User:
    def __init__(self, user_id: Union[str, int], role: UserRole, nickname: str):
        self.id = str(user_id)
        self.role = role
        self.nickname = nickname

    def to_dict(self):
        return {
            'role': self.role.value,
            'nickname': self.nickname
        }

    def has_role(self, role: UserRole):
        return self.role == role

    def __str__(self):
        return f"User(id={self.id}, role={self.role.value}, nickname={self.nickname})"
@singleton
class UserManager:
    def __init__(self):
        self.data = {}
        self.filename = FileNamesEnum.USERS_DATA.value
        self.data_changed = False

    async def initialize(self, load_func: Callable[[str], Dict] = load):
        try:
            print("загрузка из файла")
            loaded_data = load_func(self.filename)  # Используем переданную функцию load
            for user_id, user_info in loaded_data.items():
                role_str = user_info['role']
                role = UserRole.__getitem__(role_str)  # Приводим к верхнему регистру
                if role is None:
                    raise ValueError(f"Неизвестная роль: {role_str}")
                self.data[user_id] = User(user_id, role, user_info['nickname'])
        except FileNotFoundError:
            print("Файл не найден, инициализируем данные по умолчанию.")
            self.data_changed = True
            await self.save_data()  # Сохраняем начальные данные в файл

    async def save_data(self, save_func: Callable[[Dict, str], None] = save):
        if self.data_changed:  # Проверяем, были ли изменения
            async with lock:  # test LOCK
                try:
                    save_data = {user.id: user.to_dict() for user in self.data.values()}
                    save_func(save_data, self.filename, overwrite=True)  # Используем переданную функцию save
                    self.data_changed = False  # Сбрасываем флаг после сохранения
                    print("Данные сохранены.")
                except Exception as e:
                    print(f"Ошибка при сохранении данных: {e}")

    def delete_all_users(self):
        self.data = {}
        self.data_changed = True

    def get_user_by_id(self, user_id: Union[str, int]) -> Union[User, None]:
        return self.data.get(str(user_id), None)  # Возвращаем пользователя или None

    def create_user(self, user_id: Union[str, int], nickname: str, role: UserRole) -> Union[User, None]:
        user_id = str(user_id)
        if self.get_user_by_id(user_id) is not None:
            print("Такой пользователь уже есть")
            return

        new_user = User(user_id, role, nickname)
        self.data[user_id] = new_user
        self.data_changed = True  # Устанавливаем флаг изменений
        print(f"user created, id = {user_id}")
        return new_user

    def change_user_role(self, user_id: Union[str, int], new_role: UserRole):
        user_id = str(user_id)
        user = self.get_user_by_id(user_id)
        if user is None:
            print("User not found.")
            return

        user.role = new_role
        self.data_changed = True  # Устанавливаем флаг изменений

    def delete_user(self, user_id: Union[str, int]):
        user_id = str(user_id)
        try:
            del self.data[user_id]
            self.data_changed = True  # Устанавливаем флаг изменений
        except KeyError:
            raise ValueError("User not found.")  # Выбрасываем исключение, если пользователь не найден

    def get_user_role(self, user_id: Union[str, int]) -> Union[UserRole, None]:
        user = self.get_user_by_id(user_id)
        if user is not None:
            return user.role  # Возвращаем роль пользователя
        return None  # Пользователь не найден

    def get_all_users(self) -> List[User]:
        return list(self.data.values())  # Возвращаем всех пользователей

    def count_users(self) -> int:
        return len(self.data)  # Возвращаем количество пользователей

    def get_list_users_id(self) -> List[str]:
        return list(self.data.keys())  # Возвращаем список ID пользователей

    def get_users_by_role(self, role: UserRole) -> List[User]:
        """Возвращает список пользователей с заданной ролью."""
        return [user for user in self.data.values() if user.role == role]

    def get_data_format(self) -> str:
        return json.dumps({user.id: user.to_dict() for user in self.data.values()}, indent=4)

    async def periodic_save(self, interval, save_func: Callable[[Dict, str], None] = save):
        while True:
            await asyncio.sleep(interval)  # Ждем указанный интервал
            await self.save_data(save_func=save_func)  # Сохраняем данные

    async def start_async(self, load_func: Callable[[str], Dict] = load,
                          save_func: Callable[[Dict, str], None] = save):
        await self.initialize(load_func=load_func)  # Инициализация данных
        asyncio.create_task(self.periodic_save(SAVE_INTERVAL, save_func=save_func))  # Запуск фонового процесса

# Глобальная переменная для экземпляра UserManager
user_manager = UserManager()

# ДЛЯ ТЕСТА
# async def test_promts():
#     # Мини тесты
#     print("Тестирование функций управления пользователями:")
#
#     # Создание пользователей
#     user_manager.create_user("1", "Leha", UserRole.ADMIN)
#     user_manager.create_user("11", "Leha2", UserRole.ADMIN)
#     user_manager.create_user("111", "Leha3", UserRole.ADMIN)
#     user_manager.create_user("3", "Alice", UserRole.USER)
#
#     # Вывод текущих данных
#     print("Текущие данные пользователей:")
#     print([str(user) for user in user_manager.get_all_users()])
#     # print(user_manager.get_data_format())
#
# async def main_test():
#     await user_manager.start_async()
#     await test_promts()
#     # Основной цикл будет работать 10 секунд, чтобы увидеть работу фонового процесса
#     await asyncio.sleep(10)
#     print("Основная программа завершена.")
#
# if __name__ == "__main__":
#     asyncio.run(main_test())
