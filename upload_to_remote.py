import asyncio
from enums import FileNamesEnum  # Импортируйте ваши перечисления
from json_file_manager import duplicate_to_remote  # Импортируйте вашу функцию
from config import SAVE_INTERVAL_TO_REMOTE  # Импортируйте интервал сохранения
from mc_server_manager import server_data
async def copy_files_to_remote():
    while True:
        if server_data["online"]:
        # Перебираем все файлы, которые нужно скопировать
            for file_name in FileNamesEnum:
                duplicate_to_remote(file_name)  # Копируем файл на удаленный сервер

        await asyncio.sleep(SAVE_INTERVAL_TO_REMOTE)  # Ждем заданный интервал

async def start_sync_remote():
    # Запускаем задачу копирования файлов
    asyncio.create_task(copy_files_to_remote())

# Запускаем основной асинхронный цикл
if __name__ == "__main__":
    asyncio.run(start_sync_remote())
