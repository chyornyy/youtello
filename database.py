from datetime import datetime
import psycopg2
import os

conn = psycopg2.connect(f"""
    host={os.getenv('DB_HOST')}
    port={os.getenv('DB_PORT')}
    sslmode={os.getenv('DB_SSLMODE')}
    dbname={os.getenv('DB_DBNAME')}
    user={os.getenv('DB_USER')}
    password={os.getenv('DB_PASSWORD')}
    target_session_attrs={os.getenv('DB_TARGET_SESSION_ATTRS')}
""")


def register_user(TABLE, user_login, chat_id):
    """Получает в registered_users список кортежей с chat_id, проверяет есть ли chat_id пользователя, нажавшего /start и если нет - добавляет"""
    q = conn.cursor()
    q.execute('SELECT chat_id FROM registered_users')
    chat_id_list = q.fetchall()
    if (chat_id,) not in chat_id_list:
        id_data = len(chat_id_list)
        date_data = datetime.now().date()
        time_data = datetime.now().time().strftime('%H:%M')
        q.execute(f"INSERT INTO {TABLE} (id, user_login, chat_id, date, time) VALUES (%s, %s, %s, %s, %s)", (id_data, user_login, chat_id, date_data, time_data))
        conn.commit()
        print(f'Добавлен пользователь {user_login}')
    else:
        pass
    q.execute('SELECT user_login FROM registered_users')
    print(q.fetchall())


def add_command_data_to_metrics(TABLE, chat_id, command_type):
    q = conn.cursor()
    date_data = datetime.now().date()
    time_data = datetime.now().time().strftime('%H:%M')
    q.execute('SELECT chat_id FROM metrics')
    push_metrics_list = q.fetchall()
    id_data = len(push_metrics_list)
    q.execute(f"INSERT INTO {TABLE} (id, chat_id, command_type, date, time) VALUES (%s, %s, %s, %s, %s)", (id_data, chat_id, command_type, date_data, time_data))
    conn.commit()


def add_push_data_to_metrics(TABLE, chat_id, push_type):
    q = conn.cursor()
    date_data = datetime.now().date()
    time_data = datetime.now().time().strftime('%H:%M')
    q.execute('SELECT chat_id FROM metrics')
    push_metrics_list = q.fetchall()
    id_data = len(push_metrics_list)
    q.execute(f"INSERT INTO {TABLE} (id, chat_id, push_type, date, time) VALUES (%s, %s, %s, %s, %s)", (id_data, chat_id, push_type, date_data, time_data))
    conn.commit()


def get_active_users_list_for_mailing():
    q = conn.cursor()
    q.execute('SELECT chat_id FROM registered_users')
    return q.fetchall()


def check_admin():
    pass
