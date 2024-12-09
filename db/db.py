import psycopg2
from psycopg2 import sql

class DB:

    def __init__(self, db_config):

        self.db_config = db_config  # Словарь с параметрами подключения к БД
        self.connection = self.get_db_connection()

    def get_db_connection(self):
        return psycopg2.connect(
            host=self.db_config['host'],
            port=self.db_config['port'],
            database=self.db_config['database'],
            user=self.db_config['user'],
            password=self.db_config['password']
        )
    
    def create_user_task(self, command):
        conn = self.connection
        cursor = conn.cursor()
        try:
            # SQL-запрос для вставки новой записи в таблицу user_task
            insert_query = sql.SQL("INSERT INTO user_tasks (task_command) VALUES (%s) RETURNING id;")
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

        conn = self.connection
        cursor = conn.cursor()
        try:
            # SQL-запрос для вставки новой записи в таблицу node_task
            insert_query = sql.SQL("INSERT INTO node_task (user_task_id, data) VALUES (%s, %s) RETURNING id;")
            cursor.execute(insert_query, (user_task_id, task_data))

            node_task_id = cursor.fetchone()[0]
            conn.commit()
            return node_task_id  # Возвращаем ID новой задачи

        except Exception as e:
            print(f"Error while creating user task: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    def update_node_task_result(self, user_task_id, result):

        conn = self.connection
        cursor = conn.cursor()
        try:
            # SQL-запрос для вставки новой записи в таблицу node_task
            update_query = sql.SQL("UPDATE node_task SET result = %s WHERE user_task_id = %s RETURNING id;")
            cursor.execute(update_query, (result, user_task_id))

            node_task_id = cursor.fetchone()[0]
            conn.commit()
            return node_task_id  # Возвращаем ID задачи

        except Exception as e:
            print(f"Error while creating user task: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    db_config = {
        'host': '95.165.10.162',
        'port': '5432',
        'database': 'yarik',
        'user': 'yarik',
        'password': 'yarik'
    }
    
    db = DB(db_config)


    """command = 'Test data 1'
    result = 'Test_result_data 1'
    # user_task_id = db.create_user_task(command)
    # if user_task_id:
    #     print(f"User  task created with ID: {user_task_id}")

    node_task_id = db.create_node_task('3', command)
    if node_task_id:
        print(f"Node task created with ID: {node_task_id}")

    result_task = db.update_node_task_result('3', result)
    if result_task:
        print(f"Node task created with ID: {result_task}")"""