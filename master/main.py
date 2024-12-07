import asyncio
import json
from websockets import connect, WebSocketClientProtocol
from http.server import BaseHTTPRequestHandler, HTTPServer


class Scheduler:
    def push_single_node_state(self, node_id, state):
        pass

    def get_distribute_tasks(self):
        pass



class Master:
    def __init__(self, scheduler, db, node_ips):
        self.tasks = []  # Список задач для распределения
        self.node_ips = node_ips  # Список IP-адресов нод
        self.scheduler = scheduler  # Экземпляр класса Scheduler
        self.db = db  # Экземпляр класса DB
        self.node_connections = {}  # Соединения WebSocket для каждого узла
        asyncio.run(self.establish_connections())  # Устанавливаем соединения с узлами

    async def establish_connections(self):
        """Устанавливает соединение WebSocket со всеми узлами и запускает слушатель."""
        for node_id, node_ip in self.node_ips.items():
            websocket = await connect(f"ws://{node_ip}:8080")
            self.node_connections[node_id] = websocket
            asyncio.create_task(self.listen_to_node(node_id, websocket))
            print(f"Установлено соединение с узлом {node_id} ({node_ip})")

    async def listen_to_node(self, node_id, websocket):
        """Непрерывно вычитывает сообщения из WebSocket и обновляет состояние узла."""
        async for message in websocket:
            data = json.loads(message)
            state = data.get("state")
            if "done" in data:
                task_id = data["task_id"]
                result = data["result"]
                self.db.update_task_result(task_id, result)
                print(f"Задача {task_id} завершена на узле {node_id} с результатом: {result}")
            else:
                self.scheduler.push_single_node_state(node_id, state)

    async def dispatch_task_to_node(self, node_id, task_data):
        """Отправляет данные задачи узлу через уже установленное WebSocket соединение."""
        websocket: WebSocketClientProtocol = self.node_connections[node_id]
        await websocket.send(json.dumps(task_data))
        print(f"Задача {task_data['task_id']} отправлена узлу {node_id}")

    def push_tasks(self):
        """Запрашивает распределение задач у планировщика и отправляет задачи узлам."""
        task_distribution = self.scheduler.get_distribute_tasks(self.tasks)
        for node_id, tasks in task_distribution.items():
            for task_id in tasks:
                task_data = self.get_task_data(task_id)
                asyncio.run(self.dispatch_task_to_node(node_id, task_data))

    def get_task_data(self, task_id):
        """Собирает необходимую информацию для выполнения задачи."""
        # Получаем данные задачи из базы данных
        task_data = {
            "task_id": task_id,
            "data": self.db.tasks_data.get(task_id, {})
        }
        print(f"Собраны данные для задачи {task_id}: {task_data}")
        return task_data

    # --- User (HTTP) ---

    class RequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            """Принимает JSON от пользователя, создает записи в таблице user_tasks и tasks, затем отправляет задачи."""
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_info = json.loads(post_data.decode('utf-8'))

            name = task_info.get("name")
            command = task_info.get("command")
            data_list = task_info.get("data", [])

            # Создаем запись в таблице user_tasks
            master = self.server.master
            user_task_id = master.db.create_user_task(name, command)

            # Создаем записи в таблице tasks для каждого элемента в data
            for task_data in data_list:
                task_id = master.db.create_task(user_task_id, task_data)
                master.tasks.append(task_id)

            # Передаем задачи в планировщик
            master.push_tasks()

            # Возвращаем ответ клиенту
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"status": "Tasks created and distributed", "user_task_id": user_task_id}
            self.wfile.write(json.dumps(response).encode())

    def start_http_server(self):
        """Запускает HTTP-сервер для получения данных от пользователя."""
        server = HTTPServer(('localhost', 8081), self.RequestHandler)
        server.master = self
        print("HTTP-сервер запущен на порту 8081")
        server.serve_forever()


# Пример использования
node_ips = {1: "192.168.1.10", 2: "192.168.1.11"}
scheduler = Scheduler()
db = DB()
master = Master(scheduler, db, node_ips)

# Запускаем HTTP-сервер
asyncio.run(master.start_http_server())
