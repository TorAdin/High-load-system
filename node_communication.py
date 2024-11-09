import websockets
import threading
import json
import time
import psutil
from queue_proccesing import Task, QueueTask


Task = Task()
QueueTask = QueueTask()


class NodeCommunication:
    def __init__(self, master_url, node_id):
        self.master_url = master_url
        self.node_id = node_id
        self.websocket_master = None
        self.lock = threading.Lock()
        self.stop_event = threading.Event()

    # Подключение к мастер-ноде
    def connect_to_master(self):
        try:
            self.websocket_master = websockets.client.connect(self.master_url)
            print(f'Подключен к мастеру: {self.websocket_master=}')
        except Exception as e:
            print(f'Ошибка при подключении к мастеру: {e}')

    # Регистрация ноды
    def register_node(self):
        try:
            registration_message = json.dumps({
                "type": "register",
                "node_id": self.node_id
            })
            self.websocket_master.send(registration_message)
            print("Регистрация ноды отправлена")
        except Exception as e:
            print(f"Ошибка при регистрации ноды: {e}")

    # Получение задачи от мастера
    def wait_for_task_json(self):
        while not self.stop_event.is_set():
            if self.websocket_master is not None:
                try:
                    self.check_master_connection()
                    task_json = self.websocket_master.recv()
                    print(f'Получены данные от мастера {task_json=}')
                    Task.status("accepted")

                    task_json = json.loads(task_json)
                    task_id = task_json.get("task_id")
                    data_id = task_json.get("id_data")

                    all_data = get_from_data_base(task_id, data_id)

                    with self.lock:
                        Task.put_to_queue(task_id, all_data)
                        print(f'Задача {task_id} отправлена в очередь')

                except Exception as e:
                    print(f'Ошибка при получении данных {e}')

    # Получение результатов задачи
    def get_results(self):
        while not self.stop_event.is_set():
            with self.lock:
                results = Task.get_results()
                if results is not None:
                    task_id = results.get("task_id")
                    data_id = results.get("data_id")

                    print(f'Получены результаты задачи {task_id}')
                    Task.status = "done"
                    self.send_results(task_id, data_id, results)

    # Отправка результатов задачи
    def send_results(self, task_id, data_id, results):
        try:
            result_message = json.dumps({
                "type": "result",
                "task_id": task_id,
                "data_id": data_id,
                "results": results
            })
            self.websocket_master.send(result_message)
            print(f"Результаты задачи {task_id} отправлены")
        except Exception as e:
            print(f"Ошибка при отправке результатов задачи: {e}")

    # Проверка статуса ноды
    def get_node_status(self):
        try:
            status = Task.status
            q_size = QueueTask.len_queue()

            status_message = json.dumps({
                "type": "status",
                "node_id": self.node_id,
                "status": status,
                "queue_size": q_size
            })
            self.check_master_connection()
            self.websocket_master.send(status_message)

            print(f"Статус ноды отправлен")
        except Exception as e:
            print(f"Ошибка при запросе статуса ноды: {e}")

    # Проверка доступности мастер-ноды
    def check_master_connection(self):
        try:
            if not self.websocket_master.open:
                print("Соединение с мастер-нодой потеряно, попытка переподключения...")
                self.reconnect_to_master()
        except Exception as e:
            print(f"Ошибка при проверке соединения с мастером: {e}")

    # Переподключение к мастер-ноде
    def reconnect_to_master(self, retries=5):
        for attempt in range(retries):
            try:
                self.connect_to_master()
                if self.websocket_master is not None:
                    print("Успешное переподключение к мастер-ноде")
                    return
            except Exception as e:
                print(f"Попытка {attempt + 1} из {retries} не удалась: {e}")
                time.sleep(5)
        print("Не удалось переподключиться к мастер-ноде")

    # Запуск потоков
    def start(self):
        try:
            self.connect_to_master()

            self.register_node()

            task_thread = threading.Thread(target=self.wait_for_task_json)
            results_thread = threading.Thread(target=self.get_results)

            task_thread.start()
            results_thread.start()

            task_thread.join()
            results_thread.join()
        except KeyboardInterrupt:
            self.stop_event.set()
            print("Остановка работы")


def get_from_data_base(task_id, data_id):
    first_id = data_id.get("first")
    last_id = data_id.get("last")

    all_data = {'i': [1, 2, 3, 4]}  # pupupu

    return all_data


if __name__ == "__main__":
    node = NodeCommunication(master_url="ws://localhost:8000", node_id="node_1")
    node.start()
