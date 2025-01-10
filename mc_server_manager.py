import re
import time
import socket
import asyncio
from mcrcon import MCRcon
from config import SERVER_IP, SERVER_PORT, RCON_PASSWORD, PING_INTERVAL, REQUEST_COOLDOWN
import json_file_manager
from enums import FileNamesEnum
# Глобальные переменные
server_data = {
    "online": False,
    "rcon_data": {
        "list": {"current_players": 0,
                "max_players": 0,
                "list_players": []}
    },
    "time": None
}

last_request_time = 0

def ping_server():
    online = False
    try:
        with socket.create_connection((SERVER_IP, SERVER_PORT), timeout=1):
            online = True
    except (socket.timeout, ConnectionRefusedError):
        online = False
    
    return online
def can_make_request():
    global last_request_time
    current_time = time.time()
    return (current_time - last_request_time) >= REQUEST_COOLDOWN

def get_rcon_data(command):
    global last_request_time
    try:
        with MCRcon(SERVER_IP, RCON_PASSWORD, port=SERVER_PORT) as mcr:
            response = mcr.command(command)
            return response
    except Exception as e:
        return f"Ошибка при выполнении команды RCON: {e}"
    
def parse_rcon_list_response(to_write_data):
    response = get_rcon_data("list")
    # Удаляем символы новой строки и лишние пробелы
    response = response.strip()

    # Используем регулярное выражение для извлечения информации
    match = re.search(r'There are (\d+) of a max of (\d+) players online: ?(.*)', response)
    
    if match:
        current_players = int(match.group(1))  # Текущее количество игроков
        max_players = int(match.group(2))      # Максимальное количество игроков
        player_list = match.group(3).split(', ') if match.group(3) else []  # Список игроков, разделенный запятой
        if to_write_data:
            server_data["rcon_data"]["list"] = {}
            server_data["rcon_data"]["list"]["current_players"] = current_players
            server_data["rcon_data"]["list"]["max_players"] = max_players
            server_data["rcon_data"]["list"]["list_players"] = player_list
        return current_players, max_players, player_list
    else:
        return None  # Если парсинг не удался

def update_all_data(check_last_upd_time): #Данные которые должны обновляться всегда - онлайн ли сервер? кол-во игроков сейчас и так далее
    global last_request_time
    if check_last_upd_time and not can_make_request():
        print("Подождите, чтобы сделать новый запрос.")
        return
    ping = ping_server()
    #какие нибудь функции, записывающие данные
    parse_rcon_list_response(True)
    #
    if check_last_upd_time:
        last_request_time = time.time()
        server_data["online"] = ping
        server_data["time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_request_time))
        return True
    return False

async def update_data_async():
    while True:
        if ping_server():
            if update_all_data(True):  # Пример команды для получения количества игроков
                json_file_manager.save(server_data, FileNamesEnum.SERVER_STATS, True)
        else:
            print("сервер оффлайн")
        await asyncio.sleep(PING_INTERVAL)  # Используем await для асинхронного ожидания

async def start_async(): 
    asyncio.create_task(update_data_async())  # Запускаем асинхронную задачу



# def update_data():
#     while True:
#         if ping_server():
#             if update_all_data(True):  # Пример команды для получения количества игроков
#                 json_file_manager.save(server_data, FileNamesEnum.SERVER_STATS, True)
#         else:
#             print("сервер оффлайн")
#         time.sleep(PING_INTERVAL)
#         print(server_data)

# if __name__ == "__main__":
#     update_data()
