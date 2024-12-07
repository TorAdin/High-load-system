from psycopg2 import sql

class DB:
    def __init__(self):
        self.tasks = {}  # Таблица задач
        self.user_tasks = {}  # Таблица пользовательских задач

        self.db_config = db_config  # Словарь с параметрами подключения к БД
        self.connection = self.get_db_connection()

    def get_db_connection(self):
        return psycopg2.connect(
            host=self.db_config['host'],
            database=self.db_config['database'],
            user=self.db_config['user'],
            password=self.db_config['password']
        )
    
    def create_user_task(self, command):
        conn = self.connection
        cursor = conn.cursor()
        try:
            # SQL-запрос для вставки новой записи в таблицу user_task
            insert_query = sql.SQL("(command) RETURNING id;")
            cursor.execute(insert_query, (command,))
            
            user_task_id = cursor.fetchone()[0]  # Получаем ID созданной записи
            conn.commit()  # Подтверждаем изменения
            return user_task_id  # Возвращаем ID новой задачи
        except Exception as e:
            print(f"Error while creating user task: {e}")
            conn.rollback()  # Откатываем изменения в случае ошибки
            return None
        finally:
            cursor.close()
            conn.close()


    def create_node_task(self, user_task_id, task_data):
        pass

    def update_node_task_result(self, task_id, result):
        pass



    if __name__ == "__main__":
    db_config = {
        'host': '95.165.10.162',
        'port': '5432'
        'database': 'yarik',
        'user': 'yarik',
        'password': 'yarik'
    }
    
    db = DB(db_config)
    command = "INSERT  FROM user_tasks;"
    user_task_id = db.create_user_task(command)
    if user_task_id:
        print(f"User  task created with ID: {user_task_id}")