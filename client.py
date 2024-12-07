import json
import os
import requests

def prepare_json(data=None, files=None, user_code=None):
    """
    Формирует JSON с данными, файлами и пользовательским кодом.
    :param data: Данные, введённые пользователем.
    :param files: Список путей к файлам.
    :param user_code: Пользовательский код.
    :return: JSON-структура.
    """
    file_data = []
    if files:
        for file_path in files:
            try:
                with open(file_path, 'r') as file:
                    file_data.append({
                        "file_name": os.path.basename(file_path),
                        "content": file.read()
                    })
            except Exception as e:
                print(f"Ошибка при чтении файла {file_path}: {e}")

    # Формирование payload
    payload = {
        "data": data if data else [],
        "files": file_data,
        "user_code": user_code  # Передаём пользовательский код
    }
    return json.dumps(payload)

def send_to_master_node(json_payload, master_node_url):
    """
    Отправляет JSON на мастер-ноду.
    :param json_payload: JSON-структура.
    :param master_node_url: URL мастер-ноды.
    :return: Ответ от мастер-ноды.
    """
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(master_node_url, data=json_payload, headers=headers)
        response.raise_for_status()  # Проверка HTTP-статуса
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке данных на мастер-ноду: {e}")
        return None
