import paramiko
from config import SERVER_IP, SSH_USER, SSH_KEY_PATH, SSH_DATA_PATH


def create_ssh_client(server_ip=SERVER_IP, ssh_user=SSH_USER, ssh_key_path=SSH_KEY_PATH):
    """Создает и возвращает SSH клиент."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(server_ip, username=ssh_user, key_filename=ssh_key_path, timeout=1)
        return ssh
    except paramiko.ssh_exception.NoValidConnectionsError:
        raise ConnectionError(f"Не удалось подключиться к серверу {server_ip}. Сервер недоступен.")
    except paramiko.ssh_exception.AuthenticationException:
        raise ValueError("Ошибка аутентификации. Проверьте имя пользователя и ключ.")
    

def upload_file_to_remote(ssh_client, local_file_path, remote_file_name):
    """Загружает файл на удаленный сервер через SFTP."""
    with ssh_client.open_sftp() as sftp:
        sftp.put(local_file_path, SSH_DATA_PATH + remote_file_name)

def execute_ssh_command(ssh_client, command):
    """Выполняет произвольную команду на удаленном сервере через SSH."""
    stdin, stdout, stderr = ssh_client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()  # Ждем завершения команды

    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')

    if exit_status == 0:
        return output
    else:
        raise Exception(f"Ошибка выполнения команды: {error}")

def suspend_remote_machine(ssh_client):
    """Выключает удаленный компьютер через SSH."""
    command = 'sudo systemctl suspend'  # Команда для немедленного выключения
    try:
        execute_ssh_command(ssh_client, command)
        print("Команда на выключение отправлена.")
    except Exception as e:
        print(f"Ошибка при попытке выключить удаленный компьютер: {e}")

# Пример использования
if __name__ == "__main__":
    try:
        ssh_client = create_ssh_client()

        # Пример выполнения команды
        command_output = execute_ssh_command(ssh_client, 'ls -l')
        command_output = execute_ssh_command(ssh_client, './sleep_server.sh')
        print("Вывод команды:", command_output)

        # Выключение удаленного компьютера
        suspend_remote_machine(ssh_client)
    finally:
        ssh_client.close()
