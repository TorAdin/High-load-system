import json
import os
import requests

def prepare_json(data=None, files=None, user_code=None):
    
    file_data = []
    if files:
        for file_path in files:
            try:
                with open(file_path, 'r') as file:
                    file_data.append([
                        os.path.basename(file_path),  # Название файла
                        file.read()  # Содержимое файла
                    ])
            except Exception as e:
                print(f"Ошибка при чтении файла {file_path}: {e}")

    # Формирование payload
    payload = {
        "data": data if data else [],
        "files": file_data,  # Список массивов: [название, содержимое]
        "user_code": user_code  # Передаём пользовательский код
    }
    return json.dumps(payload)

def send_to_master_node(json_payload, master_node_url):
    
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(master_node_url, data=json_payload, headers=headers)
        response.raise_for_status()  # Проверка HTTP-статуса
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке данных на мастер-ноду: {e}")
        return None
