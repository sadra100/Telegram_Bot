import sqlite3
from config import DATABASE_PATH

def initialized_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT
        )
''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        message TEXT,
        timestamp DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON users (user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON messages (id)')

    conn.commit()
    conn.close()


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

def save_message(user_id,message):
    conn=sqlite3.connect(DATABASE_PATH)
    cursor=conn.cursor()
    cursor.execute('''
        INSERT INTO messages(user_id,message)
        VALUES(?,?)
    ''',(user_id,message))
    conn.commit()
    conn.close()

