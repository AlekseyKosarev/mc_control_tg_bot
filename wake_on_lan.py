from wakeonlan import send_magic_packet
from config import SERVER_MAC

def wake_on_lan():
    send_magic_packet(SERVER_MAC)

if __name__ == "__main__":
        wake_on_lan()
