import subprocess
import logging
from config import SERVER_IP, SSH_USER, SSH_KEY_PATH, SSH_DATA_PATH

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_ssh_command(command):#"-o", "StrictHostKeyChecking=no",
    """Создает команду SSH для выполнения."""
    return f'ssh -o StrictHostKeyChecking=no -i {SSH_KEY_PATH} {SSH_USER}@{SERVER_IP} "{command}"'

def upload_file_to_remote(local_file_path, remote_file_name):
    """Загружает файл на удаленный сервер через SCP."""
    scp_command = f'scp -o StrictHostKeyChecking=no -i {SSH_KEY_PATH} {local_file_path} {SSH_USER}@{SERVER_IP}:{SSH_DATA_PATH}{remote_file_name}'
    try:
        # logging.info(f"Загрузка файла {local_file_path} на {SSH_DATA_PATH}{remote_file_name}...")
        subprocess.run(scp_command, shell=True, check=True)
        logging.info(f"Файл {local_file_path} успешно загружен на {SSH_DATA_PATH}{remote_file_name}.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при загрузке файла: {e}")

def execute_ssh_command(command):
    """Выполняет произвольную команду на удаленном сервере через SSH."""
    ssh_command = create_ssh_command(command)
    try:
        logging.info(f"Выполнение команды: {ssh_command}")
        result = subprocess.run(ssh_command.split(), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        logging.info(f"Вывод команды: {output}")
        return output
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка выполнения команды: {e.stderr.decode('utf-8')}")
        raise Exception(f"Ошибка выполнения команды: {e.stderr.decode('utf-8')}")


def suspend_remote_machine():
    """Выключает удаленный компьютер через SSH."""
    command = 'sudo systemctl suspend'  # Команда для приостановки
    try:
        logging.info("Отправка команды на приостановку удаленного компьютера...")
        execute_ssh_command(command)
        logging.info("Команда на приостановку отправлена.")
    except Exception as e:
        logging.error(f"Ошибка при попытке приостановить удаленный компьютер: {e}")

# Пример использования
if __name__ == "__main__":
    #Вывод конфигурационных параметров
    logging.info(f"Конфигурация: SERVER_IP={SERVER_IP}, SSH_USER={SSH_USER}, SSH_KEY_PATH={SSH_KEY_PATH}, SSH_DATA_PATH={SSH_DATA_PATH}")
    #
    # try:
    #     # Пример выполнения команды
    #     command_output = execute_ssh_command('ls')
    #     #print("Вывод команды:", command_output)
    # except Exception as e:
    #     logging.error(f"Произошла ошибка: {e}")
