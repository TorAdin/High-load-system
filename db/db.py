import psycopg2
from psycopg2 import sql
import time

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
    
    # CREATE user_task IN TABLE user_tasks -> user_task_id
    def create_user_task(self, command: str) -> int:
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

    # CREATE NODE IN TABLE node_task -> node_task_id
    def create_node_task(self, user_task_id: int, task_data: str) -> int:

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
            print(f"Error while creating node_task: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    # UPDATE result IN TABLE node_task -> node_task_id
    def update_node_task_result(self, user_task_id: int, result: str) -> int:

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
            print(f"Error while updating result in node_task: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    # UPDATE node_id IN TABLE node_task -> node_task_id
    def update_node_task_node_id(self, user_task_id: int, node_id: int) -> int:

        conn = self.connection
        cursor = conn.cursor()
        try:
            # SQL-запрос для вставки новой записи в таблицу node_task
            update_query = sql.SQL("UPDATE node_task SET node_id = %s WHERE user_task_id = %s RETURNING id;")
            cursor.execute(update_query, (node_id, user_task_id))

            node_task_id = cursor.fetchone()[0]
            conn.commit()
            return node_task_id  # Возвращаем ID задачи

        except Exception as e:
            print(f"Error while updating node_id in node_task: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()
    
    
    # UPDATE STATUS(default planned -> awaits -> at_work -> completed) -> node_task_id
    def update_node_task_status(self, user_task_id: int, status: str) -> int:

        conn = self.connection
        cursor = conn.cursor()
        try:
            # SQL-запрос для вставки новой записи в таблицу node_task
            update_query = sql.SQL("UPDATE node_task SET status = %s WHERE user_task_id = %s RETURNING id;")
            cursor.execute(update_query, (status, user_task_id))

            node_task_id = cursor.fetchone()[0]
            conn.commit()
            return node_task_id  # Возвращаем ID задачи

        except Exception as e:
            print(f"Error while updating status in node_task: {e}")
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
    '''
    command = 'test data 5'
    data = 'Test data 4'
    result = 'Test_result_data 2'

    user_task_id = db.create_user_task(command)
    print(f"User  task created with ID: {user_task_id}")
    

    print(f"Node task created with ID: {db.create_node_task(6, data)}")

    print(f"Node result updated with ID: {db.update_node_task_result(user_task_id, result)}")
    
    print(f"Node task_id updated with ID: {db.update_node_task_node_id(3, 20)}")
    
    print(f"Node task_id updated with ID: {db.update_node_task_status(3, 'at_work')}")
    '''
