import json
import os
import datetime
from config import LOCAL_DATA_PATH
from enums import FileNamesEnum
from ssh_utils import upload_file_to_remote
def get_file_path(file_name, return_with_local_path=True):
    """Возвращает путь к файлу из строки или Enum."""
    local_path = ""
    if return_with_local_path:
        local_path = LOCAL_DATA_PATH

    if isinstance(file_name, FileNamesEnum):
        return local_path+file_name.value
    return local_path+file_name  # Предполагаем, что это строка

def load(file_name):
    """Загружает данные из JSON файла. Принимает строку или Enum."""
    file_path = get_file_path(file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except IOError as e:
        raise RuntimeError(f"Ошибка при чтении файла {file_path}: {e}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Ошибка при декодировании JSON из файла {file_path}: {e}")

def save(data, file_name, overwrite=False):
    """Сохраняет данные в JSON файл. Если overwrite=True, перезаписывает файл."""
    file_path = get_file_path(file_name)

    if not overwrite and os.path.exists(file_path):
        raise FileExistsError(f"Файл {file_path} уже существует. Установите overwrite=True для перезаписи.")
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        raise RuntimeError(f"Ошибка при записи в файл {file_path}: {e}")

def delete(file_name):
    """Удаляет JSON файл."""
    file_path = get_file_path(file_name)

    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        raise FileNotFoundError(f"Файл {file_path} не найден.")

def duplicate_to_remote(file_name, use_datetime=True):
    """Дублирует файл на удаленный сервер через SSH."""

    file_path = get_file_path(file_name)

    new_file_name = file_path
    if use_datetime:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        new_file_name = f"{new_file_name}_{timestamp}.json"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден для дублирования.")
    # ssh utils
    upload_file_to_remote(file_path, os.path.basename(new_file_name))
    # print(f"Файл {os.path.basename(new_file_name)} успешно загружен на удаленный сервер.")