from client import prepare_json, send_to_master_node

# Пример задач
tasks = [
    {"function": "sum", "parameters": {}},
    {"function": "multiply", "parameters": {"factor": 2}}
]

# Пример данных
data = [1, 2, 3, 4, 5]

# Формирование JSON
json_payload = prepare_json(tasks, data)

master_node_url = "http://master-node/api/tasks" """ URL мастер ноды """

# Отправка данных и вывод ответа
print("Отправляем данные...")
response = send_to_master_node(json_payload, master_node_url)
print("Ответ от мастер-ноды:", response)