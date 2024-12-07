import asyncio
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import psycopg2
from psycopg2.extras import RealDictCursor


class Scheduler:
    def push_single_node_state(self, node_id, state):
        pass

    def get_distribute_tasks(self, tasks):
        # Логика для распределения задач по узлам
        pass


class DB:
    def __init__(self, db_name, user, password, host="localhost", port=5432):
        """Инициализация соединения с бд"""
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def get_task(self, task_id):
        """Получает информацию о задаче и связанных строках из базы данных по ее ID."""
        # Запрос на получение основной информации задачи по ID
        task_query = f"select id, data_id from tasks where id == {task_id}"
        self.cursor.execute(task_query, (task_id,))
        id_ = self.cursor.fetchone()

        if id_ is None:
            print(f"Задача с ID {task_id} не найдена.")
            return None

        # Запрос для получения данных, связанных с этой задачей
        related_data_query = f"select idd_ from task_data where id == {task_id}"
        self.cursor.execute(related_data_query, (task_id,))
        related_data = self.cursor.fetchall()

        # Формируем результат - (related_data - массив из айдишников подмассивов, относящихся к task_id
        result = {
            "task_id": id_,
            "related_data": related_data
        }
        return result

    def update_task_result(self, task_id, data_id, result):
        """Обновляет результат выполнения задачи в базе данных."""
        update_query = f"update tasks set result = result where id == task_id and ddi == {data_id}"
        self.cursor.execute(update_query, (result, task_id))
        print(f"Задача {task_id} обновлена с результатом: {result}")

    def close(self):
        """Закрывает соединение с базой данных."""
        self.cursor.close()
        self.connection.close()


class Master:
    def __init__(self, scheduler, db, node_ips):
        self.node_ips = node_ips  # Список IP-адресов нод
        self.scheduler = scheduler  # Экземпляр класса Scheduler
        self.db = db  # Экземпляр класса DB
        self.node_connections = {}  # Соединения TCP для каждого узла

    async def establish_connections(self):
        """Устанавливает TCP соединения со всеми узлами и запускает слушатель."""
        for node_id, node_ip in self.node_ips.items():
            reader, writer = await asyncio.open_connection(node_ip, 8080)
            self.node_connections[node_id] = (reader, writer)
            asyncio.create_task(self.listen_to_node(node_id, reader))
            print(f"Установлено TCP соединение с узлом {node_id} ({node_ip})")

    async def listen_to_node(self, node_id, reader):
        """Непрерывно вычитывает сообщения из TCP сокета и обновляет состояние узла."""
        while True:
            try:
                data = await reader.read(1024)
                if not data:
                    break  # Соединение закрыто
                message = json.loads(data.decode())
                state = message.get("state")
                if "done" in message:
                    task_id = message["task_id"]
                    result = message["result"]
                    self.db.update_task_result(task_id, result)
                    print(f"Задача {task_id} завершена на узле {node_id} с результатом: {result}")
                else:
                    self.scheduler.push_single_node_state(node_id, state)
            except ConnectionResetError:
                print(f"Соединение с узлом {node_id} потеряно.")
                break

    async def dispatch_task_to_node(self, node_id, task_data):
        """Отправляет данные задачи узлу через установленное тисипи соединение"""
        _, writer = self.node_connections[node_id]
        writer.write(json.dumps(task_data).encode())
        await writer.drain()
        print(f"Задача {task_data['task_id']} отправлена узлу {node_id}")

    async def push_task(self, task_id):
        """Получает задачу по айди, распределяет и отправляет ее узлам"""
        task_data = self.db.get_task(task_id)
        if task_data:
            task_distribution = self.scheduler.get_distribute_tasks({task_id: task_data})
            for node_id, tasks in task_distribution.items():
                for task_id, task_data in tasks.items():
                    await self.dispatch_task_to_node(node_id, task_data)
        else:
            print(f"Задача с ID {task_id} не найдена.")

    # --- User (HTTP) ---

    class RequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            """Принимает JSON с ID задачи, находит задачу и распределяет её по узлам."""
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_info = json.loads(post_data.decode('utf-8'))

            task_id = task_info.get("task_id")
            master = self.server.master

            # Проверяем, существует ли задача
            task_data = master.db.get_task(task_id)
            if not task_data:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                response = {"status": "Task not found"}
                self.wfile.write(json.dumps(response).encode())
                return

            # Передаем задачу в планировщик
            asyncio.create_task(master.push_task(task_id))

            # Возвращаем ответ клиенту
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"status": "Task distributed", "task_id": task_id}
            self.wfile.write(json.dumps(response).encode())

    def start_http_server(self):
        """Запускает HTTP-сервер для получения данных от пользователя."""
        server = HTTPServer(('localhost', 8081), self.RequestHandler)
        server.master = self
        print("HTTP-сервер запущен на порту 8081")
        server.serve_forever()

# Пример использования
# node_ips = {1: "192.168.1.10", 2: "192.168.1.11"}
# scheduler = Scheduler()
# db = DB()
# master = Master(scheduler, db, node_ips)


# Запускаем асинхронные задачи для соединений и HTTP-сервер
# async def main():
#     await master.establish_connections()
#     master.start_http_server()


# Запуск основного асинхронного контекста
# asyncio.run(main())
