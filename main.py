from client import prepare_json, send_to_master_node
import os



# Выбор: данные вводятся пользователем или загружаются из файлов
print("Выберите способ ввода данных:")
print("1. Ввести данные вручную")
print("2. Загрузить файлы")

choice = input("Ваш выбор (1/2): ")

data = None
file_paths = []

if choice == "1":
    # Ввод данных вручную
    raw_data = input("Введите данные через запятую (например, 1, 2, 3):\n").strip()
    if raw_data:
        code = [int(x.strip()) for x in raw_data.split(",") if x.strip().isdigit()]
    else:
        print("Ошибка: Данные не введены. Завершаем программу.")
        exit()
elif choice == "2":
    # Ввод пути к файлу вручную
    print("Выберите способ загрузки файла:")
    print("1. Ввести путь к файлу вручную.")
    
    file_choice = input("Ваш выбор (1/2): ").strip()
    if file_choice == "1":
        file_path = input("Введите полный путь к файлу:\n").strip()
        if os.path.isfile(file_path):
            file_paths.append(file_path)
        else:
            print(f"Ошибка: Файл по пути '{file_path}' не найден.")
            exit()
    else:
        print("Неверный выбор. Завершаем программу.")
        exit()


# Ввод пользовательского кода
print("Введите код Python, который вы хотите выполнить над данными в формате code = [] ")
user_code = input("Ваш код (например, code = [x * 2 for x in data]):\n").strip()
if not user_code:
    print("Ошибка: Код не введён. Завершаем программу.")
    exit()

# Формирование JSON
json_payload = prepare_json(data=data, files=file_paths, user_code=user_code)

# URL мастер-ноды
master_node_url = "http://master-node/api/tasks"

# Отправка данных и вывод ответа
print("\nJSON для отправки:")
print(json_payload)

print("\nОтправляем данные...")
response = send_to_master_node(json_payload, master_node_url)
if response:
    print("Ответ от мастер-ноды:", response)
else:
    print("Не удалось получить ответ от мастер-ноды.")

print("Данные файла:")
