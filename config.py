import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Server info and RCON
SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
RCON_PASSWORD = os.getenv("RCON_PASSWORD")
PING_INTERVAL = int(os.getenv("PING_INTERVAL", 10))
REQUEST_COOLDOWN = int(os.getenv("REQUEST_COOLDOWN", 10))

# WoL
PING_WAIT = int(os.getenv("PING_WAIT", 15))
SERVER_MAC = os.getenv("SERVER_MAC")

# Save manager
LOCAL_DATA_PATH = os.getenv("LOCAL_DATA_PATH", os.path.dirname(os.path.abspath(__file__)) + os.sep)
SAVE_INTERVAL_TO_REMOTE = int(os.getenv("SAVE_INTERVAL_TO_REMOTE", 1800))

# SSH settings for save to remote
SSH_USER = os.getenv("SSH_USER")
SSH_DATA_PATH = os.getenv("SSH_DATA_PATH")
SSH_KEY_PATH = os.getenv("SSH_KEY_PATH", LOCAL_DATA_PATH + "id_rsa")

# Users
SAVE_INTERVAL = int(os.getenv("SAVE_INTERVAL", 10))
def print_config():
    config_data = {
        "BOT_TOKEN": BOT_TOKEN,
        "SERVER_IP": SERVER_IP,
        "SERVER_PORT": SERVER_PORT,
        "RCON_PASSWORD": RCON_PASSWORD,
        "PING_INTERVAL": PING_INTERVAL,
        "REQUEST_COOLDOWN": REQUEST_COOLDOWN,
        "PING_WAIT": PING_WAIT,
        "SERVER_MAC": SERVER_MAC,
        "LOCAL_DATA_PATH": LOCAL_DATA_PATH,
        "SAVE_INTERVAL_TO_REMOTE": SAVE_INTERVAL_TO_REMOTE,
        "SSH_USER": SSH_USER,
        "SSH_DATA_PATH": SSH_DATA_PATH,
        "SSH_KEY_PATH": SSH_KEY_PATH,
        "SAVE_INTERVAL": SAVE_INTERVAL,
    }

    for key, value in config_data.items():
        print(f"{key}: {value}")
