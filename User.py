import json
import os

class User:
    def __init__(self):

        list_of_data = []
        folder_path = '/data'

        for filename in os.listdir(folder_path):

            file_path = os.path.join(folder_path, filename)    # Проверка, является ли текущий элемент файлом (а не подпапкой)
            if os.path.isfile(file_path):
                list_of_data.append(file_path)
                print(list_of_data)


        data = {'task': 'task/task.py', 'data': list_of_data}
        print(data)
        with open('data.json', 'w') as file:
            json.dump(data, file)

qwerty = User()
