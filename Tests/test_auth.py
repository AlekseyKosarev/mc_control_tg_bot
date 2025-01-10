import unittest
import asyncio
from unittest import mock
from enums import UserRole, FileNamesEnum
from auth import user_manager  # Импортируем экземпляр user_manager

class TestUserManagement(unittest.TestCase):
    @classmethod
    @mock.patch('json_file_manager.load')
    @mock.patch('json_file_manager.save')
    def setUpClass(cls, mock_save, mock_load):
        # Настройка мока для функции загрузки
        mock_load.return_value = {}  # Начальные данные пустые
        asyncio.run(user_manager.initialize(load_func=mock_load))  # Инициализация user_manager

    def setUp(self):
        # Сбрасываем данные перед каждым тестом
        user_manager.delete_all_users()

    def test_create_user(self):
        user_manager.create_user("1", "Leha", UserRole.ADMIN)
        self.assertEqual(user_manager.count_users(), 1)
        self.assertIsNotNone(user_manager.get_user_by_id("1"))

    def test_create_duplicate_user(self):
        user_manager.create_user("1", "Leha", UserRole.ADMIN)
        user_manager.create_user("1", "Leha", UserRole.ADMIN)  # Дублируем
        self.assertEqual(user_manager.count_users(), 1)  # Количество пользователей не должно измениться

    def test_change_user_role(self):
        user_manager.create_user("1", "Leha", UserRole.ADMIN)
        user_manager.change_user_role("1", UserRole.USER)
        self.assertEqual(user_manager.get_user_role("1"), UserRole.USER)

    def test_change_nonexistent_user_role(self):
        user_manager.change_user_role("999", UserRole.USER)  # Не существующий пользователь
        self.assertEqual(user_manager.count_users(), 0)  # Количество пользователей не должно измениться

    def test_delete_user(self):
        user_manager.create_user("1", "Leha", UserRole.ADMIN)
        user_manager.delete_user("1")
        self.assertIsNone(user_manager.get_user_by_id("1"))
        self.assertEqual(user_manager.count_users(), 0)

    def test_delete_nonexistent_user(self):
        with self.assertRaises(ValueError):
            user_manager.delete_user("999")

    def test_get_all_users(self):
        user_manager.create_user("1", "Leha", UserRole.ADMIN)
        user_manager.create_user("2", "Alice", UserRole.USER)
        users = user_manager.get_all_users()
        self.assertEqual(len(users), 2)

    def test_count_users(self):
        self.assertEqual(user_manager.count_users(), 0)
        user_manager.create_user("1", "Leha", UserRole.ADMIN)
        self.assertEqual(user_manager.count_users(), 1)

    def test_get_list_users_id(self):
        user_manager.create_user("1", "Leha", UserRole.ADMIN)
        user_manager.create_user("2", "Alice", UserRole.USER)
        user_ids = user_manager.get_list_users_id()
        self.assertIn("1", user_ids)
        self.assertIn("2", user_ids)
        self.assertEqual(len(user_ids), 2)

    def test_find_user_by_id(self):
        user_manager.create_user("1", "Leha", UserRole.ADMIN)
        user = user_manager.get_user_by_id("1")
        self.assertIsNotNone(user)
        self.assertEqual(user.id, "1")

    def test_find_nonexistent_user_by_id(self):
        user = user_manager.get_user_by_id("999")  # Не существующий пользователь
        self.assertIsNone(user)

    @mock.patch('json_file_manager.save')
    @mock.patch('json_file_manager.load')
    async def test_periodic_save(self, mock_load, mock_save):
        # Настройка мока для функции загрузки
        mock_load.return_value = {
            "1": {"role": "admin", "nickname": "Leha"}}  # Возвращаем данные, как будто они загружены

        user_manager.create_user("1", "Leha", UserRole.ADMIN)
        await user_manager.save_data()  # Сохраняем данные

        # Проверяем, что функция сохранения была вызвана
        mock_save.assert_called_once()

        # Проверяем, что данные загружаются корректно
        loaded_data = await mock_load(FileNamesEnum.USERS_DATA.value)
        self.assertIn("1", loaded_data)  # Проверяем, что данные сохранены

    @classmethod
    def tearDownClass(cls):
        # Здесь можно добавить код для очистки данных после всех тестов, если это необходимо
        # В данном случае, так как мы используем моки, ничего очищать не нужно
        pass

if __name__ == "__main__":
    unittest.main()  # Запуск тестов

