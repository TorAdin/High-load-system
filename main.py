from client import prepare_json, send_to_master_node
import os

def get_files_from_directory(directory_path):
   
    data = []
    try:
        for root, _, filenames in os.walk(directory_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if os.path.isfile(file_path):  # Проверяем, что это файл
                    data.append(file_path)
    except Exception as e:
        print(f"Ошибка при чтении файлов из папки {directory_path}: {e}")
    return data


# Выбор: данные вводятся пользователем или загружаются из файлов
print("Выберите способ ввода данных:")
print("1. Загрузить файл")
print("2. Загрузить все файлы из папки")

choice = input("Ваш выбор (1/2): ")

data = None
file_paths = []


if choice == "1":
    # Ввод пути к файлу вручную
    file_path = input("Введите полный путь к файлу:\n").strip()
    if os.path.isfile(file_path):
        file_paths.append(file_path)
    else:
        print(f"Ошибка: Файл по пути '{file_path}' не найден.")
        exit()
elif choice == "2":
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

# Выбор способа ввода пользовательского кода
print("Выберите способ ввода пользовательского кода:")
print("1. Ввести код вручную")
print("2. Загрузить код из файла")

code_choice = input("Ваш выбор (1/2): ")

user_code = None

if code_choice == "1":
    # Ввод пользовательского кода вручную
    print("Введите код Python, который вы хотите выполнить над данными:")
    user_code = input("Ваш код (например, code = [x * 2 for x in data]):\n").strip()
    if not user_code:
        print("Ошибка: Код не введён. Завершаем программу.")
        exit()
elif code_choice == "2":
    # Загрузка пользовательского кода из файла
    code_file_path = input("Введите полный путь к файлу с кодом:\n").strip()
    if os.path.isfile(code_file_path):
        try:
            with open(code_file_path, 'r') as code_file:
                user_code = code_file.read().strip()
        except Exception as e:
            print(f"Ошибка при чтении файла {code_file_path}: {e}")
            exit()
    else:
        print(f"Ошибка: Файл по пути '{code_file_path}' не найден.")
        exit()
else:
    print("Неверный выбор. Завершаем программу.")
    exit()

# Формирование JSON
json_payload = prepare_json(files=file_paths, user_code=user_code)

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
