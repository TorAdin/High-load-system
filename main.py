from client import prepare_json, send_to_master_node
import os

# Функция для получения всех файлов из папки
def get_files_from_directory(directory_path):
    
    files = []
    try:
        for root, _, filenames in os.walk(directory_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if os.path.isfile(file_path):  # Проверяем, что это файл
                    files.append(file_path)
    except Exception as e:
        print(f"Ошибка при чтении файлов из папки {directory_path}: {e}")
    return files


# Выбор: данные вводятся пользователем или загружаются из файлов
print("Выберите способ ввода данных:")
print("1. Ввести данные вручную")
print("2. Загрузить файл")
print("3. Загрузить все файлы из папки")

choice = input("Ваш выбор (1/2/3): ")

data = None
file_paths = []

if choice == "1":
    # Ввод данных вручную
    raw_data = input("Введите данные через запятую (например, 1, 2, 3):\n").strip()
    if raw_data:
        data = [int(x.strip()) for x in raw_data.split(",") if x.strip().isdigit()]
    else:
        print("Ошибка: Данные не введены. Завершаем программу.")
        exit()
elif choice == "2":
    # Ввод пути к файлу вручную
    file_path = input("Введите полный путь к файлу:\n").strip()
    if os.path.isfile(file_path):
        file_paths.append(file_path)
    else:
        print(f"Ошибка: Файл по пути '{file_path}' не найден.")
        exit()
elif choice == "3":
    # Загрузка всех файлов из папки
    directory_path = input("Введите путь к папке:\n").strip()
    if os.path.isdir(directory_path):
        file_paths = get_files_from_directory(directory_path)
        if not file_paths:
            print(f"Ошибка: В папке '{directory_path}' нет файлов.")
            exit()
    else:
        print(f"Ошибка: Папка по пути '{directory_path}' не найдена.")
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
