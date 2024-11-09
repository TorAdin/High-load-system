import queue

#класс вычислительной ноды
class CalcNode:
    def __init__(self, id, busy):
        self.id = id
        self.busy = busy
        self.qsize = 0


class Task:
    def __init__(self, id_task, name_task, data_task):
        self.id_task = id_task
        self.status = 'accepted'
        self.name_task = name_task
        self.data_task = data_task
        self.data_result = 0

    def calculate(self, data_task, func):
        self.data_result = func(data_task)
        QueueTask.history_info.append(QueueTask.arr_task.get())
        CalcNode.qsize = QueueTask.arr_task.qsize()

    def get_result(self):
        return {'id_task': self.id_task, 'name_task': self.name_task, 'data_task': self.data_task,
                'data_result': self.data_result}


class QueueTask:
    def __init__(self):
        self.arr_task = queue.Queue()
        self.history_info = []

    def print_info(self, arr_task):
        while not arr_task.empty():
            print(f'Текущие задачи в очереди: {arr_task.get().name_task}', end=' ')

    def new_data_put(self, new_task):
        self.arr_task.put(new_task)

    def len_queue(self):
        self.arr_task.qsize()

    def history_get(self):
        return self.history_info
