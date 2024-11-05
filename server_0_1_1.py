import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import sql
import os
from werkzeug.utils import secure_filename
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)  # Разрешаем CORS запросы

# Конфигурация
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Создаем папку для загрузок, если её нет
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Конфигурация базы данных PostgreSQL
DB_CONFIG = {
    'dbname': 'yarik',
    'user': 'yarik',
    'password': 'yarik',
    'host': '95.165.10.162',
    'port': '5432'
}

# Маршрут для обработки POST-запроса
@app.route('/submit', methods=['POST'])
def check_surname():
    surname = request.json.get('surname')

    # Создаем соединение с базой данных
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE surname = %s", (surname,))
            user = cursor.fetchone()

            if user:
                return jsonify({'exists': True, 'surname': surname}), 200
            else:
                cursor.execute("INSERT INTO users (surname) VALUES (%s)", (surname,))
                conn.commit()
                return jsonify({'exists': False, 'surname': surname}), 200
    except Exception as e:
        print("Ошибка:", e)
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()  # Закрываем соединениt




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})
    
    file = request.files['image']

    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Добавляем временную метку к имени файла для уникальности
        filename = f"{int(time.time())}_{filename}"

        # Сохраняем файл
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        try:
            # Сохраняем путь в базу данных
            conn = get_db_connection()
            cur = conn.cursor()

            # Сохраняем относительный путь
            db_path = f'/uploads/{filename}'
            cur.execute("INSERT INTO test_images (path) VALUES (%s)", (db_path,))
            
            conn.commit()
            cur.close()
            conn.close()

            return jsonify({
                'success': True,
                'message': 'File uploaded successfully',
                'path': db_path
            })

        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({
                'success': False,
                'message': 'Database error occurred'
            })

    return jsonify({'success': False, 'message': 'File type not allowed'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)