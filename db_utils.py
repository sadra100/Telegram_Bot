import sqlite3


def initialized_database():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT
        )
''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON users (user_id)')
    cursor.commit()
    cursor.close()


def save_user(user):
    def clean_input(text):
        return text.replace("'", '').replace('"', '').strip() if text else None

    username = clean_input(user.username)
    first_name = clean_input(user.first_name)
    last_name = clean_input(user.last_name)

    try:
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users(user_id,username,first_name,last_name)
            VALUES(?,?,?,?)
        '''), (user.id, username, first_name, last_name)
        conn.commit()


    except sqlite3.Error as e:
        print(f'Database error:{e}')

    finally:
        conn.close()
