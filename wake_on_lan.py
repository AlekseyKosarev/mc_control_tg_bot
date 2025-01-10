import socket
import time
from config import SERVER_IP, SERVER_MAC, SERVER_PORT, PING_WAIT

def wake_on_lan(macaddress, ipaddress='255.255.255.255'):
    # Преобразуем MAC-адрес в формат, необходимый для отправки
    if len(macaddress) == 17:
        macaddress = macaddress.replace(":", "").replace("-", "")
    elif len(macaddress) != 12:
        raise ValueError("Неверный формат MAC-адреса")

    # Создаем "магический" пакет
    data = bytes.fromhex('FF' * 6 + macaddress * 16)

    # Отправляем пакет на указанный IP-адрес
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(data, (ipaddress, 9))  # Порт 9 - стандартный для WoL

def is_device_online(ipaddress):
    try:
        with socket.create_connection((SERVER_IP, SERVER_PORT), timeout=1):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def wake_and_check():
    wake_on_lan(SERVER_MAC, "192.168.1.255")
    time.sleep(PING_WAIT)  # Ждем некоторое время, чтобы устройство могло включиться
    return is_device_online(SERVER_IP)

if __name__ == "__main__":
    if wake_and_check():
        print("true")
    else:
        print("false")
