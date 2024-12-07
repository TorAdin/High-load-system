import time
import random

class NodeTaskManager:
    def __init__(self):
        """
        Инициализация. Создаем пустой словарь с нодами, где ключ — id ноды, а значение — список задач.
        Каждая задача представлена словарем с названием и процентом выполнения.
        """
        self.nodes = {node_id: [] for node_id in range(1, 6)}

    def update_node_loads(self, loads):
        """
        Обновляет загруженность нод.
        :param loads: Список словарей с данными о загруженности и прогрессе выполнения задач.
                      Формат: [{"id": int, "load": float, "progress": float}, ...]
        """
        for node_data in loads:
            node_id = node_data["id"]
            progress = node_data["progress"]

            # Обновляем прогресс выполнения текущих задач
            for task in self.nodes[node_id]:
                if task["progress"] < 100:
                    task["progress"] = min(100, task["progress"] + progress)

            # Удаляем завершенные задачи
            self.nodes[node_id] = [task for task in self.nodes[node_id] if task["progress"] < 100]

    def assign_tasks(self, new_tasks):
        """
        Назначает новые задачи нодам с учетом их загруженности и количества текущих задач.
        :param new_tasks: Список новых задач в формате ["Task A", "Task B", ...].
        """
        for task_name in new_tasks:
            # Находим ноду с минимальной загруженностью (по количеству незавершенных задач)
            min_tasks_node = min(self.nodes, key=lambda node_id: len(self.nodes[node_id]))

            # Добавляем задачу к найденной ноде
            self.nodes[min_tasks_node].append({"name": task_name, "progress": 0})

    def process_input(self, loads, new_tasks):
        """
        Обрабатывает входные данные о загруженности и новых задачах.
        :param loads: Данные о загруженности и прогрессе выполнения.
        :param new_tasks: Список новых задач.
        """
        self.update_node_loads(loads)
        self.assign_tasks(new_tasks)

    def get_node_status(self):
        """
        Возвращает текущее состояние нод.
        :return: Словарь, где ключ — id ноды, значение — список задач с процентом выполнения.
        """
        return self.nodes

if __name__ == "__main__":
    manager = NodeTaskManager()

    while True:
        loads = [
            {"id": random.randint(1, 5), "load": random.uniform(0.1, 1.0), "progress": random.uniform(5, 20)}
            for _ in range(5)
        ]
        new_tasks = [f"Task {random.randint(1, 100)}" for _ in range(random.randint(1, 3))]
        manager.process_input(loads, new_tasks)
        print("Текущее состояние нод:", manager.get_node_status())
        time.sleep(5)
