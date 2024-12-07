import json

class Planner():
    def __init__(self):
        pass

    def recieve_task(self):
        #получаем и парсим задачи в очереди
        with open("file.json", "r") as file:
            nodes = json.load(file)
        nodes_tasks = {node["id"]: node["task"] for node in nodes}
        pass

    def recieve_load(self,json_data):
        #получаем загруженность нод
        with open("file.json", "r") as file:
            nodes = json.load(file)
        nodes_dict = {node["id"]: node["load"] for node in nodes}
        nodes_load_dict = {node["id"]: node["load"] * 100 for node in nodes}
        return nodes_dict
        pass

    def node_load_calculator(self, queue_size, current_task_stat, complexity):
        # queue_size - размер нынешней очереди
        # done_numb - количесвто выполенных задач на ноде
        # current_task_stat - процент выполнения данной задачи
        load_percent = queue_size * complexity + 100 * current_task_stat * complexity
        return load_percent

    def sort(self, load_dict):
        sorted_load_dict = dict(sorted(load_dict.items(), key=lambda item: item[1]))
        pass

    # def create_node_dict(n):
    #     return {i:i for i in range(n)}

    def send_plan(self):
        #Отправляем список задач далее
        pass



#На вход поступает таблица загружнности нод, которую нужно распарсить
#Необходимо на основании загруженности содержать динамическую таблицу,
#обновляемую по приходе данных
#Эта таблица задач отправляется обратно - цикл закончен