import json
import os
import requests

def prepare_json(files=None, user_code=None):
    names = []  # Список названий файлов
    data = []  # Список данных из файлов

    if files:
        for file_path in files:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()  # Чтение содержимого файла
                    # Попробуем преобразовать содержимое в список чисел
                    try:
                        file_data = [float(value) for value in content.split()]
                        names.append(os.path.basename(file_path))  # Добавляем название файла
                        data.append(file_data)  # Добавляем числовые данные
                    except ValueError:
                        print(f"Файл {file_path} содержит нечисловые данные и будет пропущен.")
            except Exception as e:
                print(f"Ошибка при чтении файла {file_path}: {e}")

    # Формирование payload
    payload = {
        # "names": names,  # Названия файлов
        "data": data,  # Числовые данные
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
