from psycopg2 import sql

class DB:
    def __init__(self):
        self.tasks = {}  # Таблица задач
        self.user_tasks = {}  # Таблица пользовательских задач

    def create_user_task(self, command):
        pass

    def create_node_task(self, user_task_id, task_data):
        pass

    def update_node_task_result(self, task_id, result):
        pass