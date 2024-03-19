import sqlite3


con = sqlite3.connect('db.sqlite', check_same_thread=False)

cur = con.cursor()




def create_table():
    query = '''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    subject TEXT,
    level TEXT,
    task TEXT,
    answer TEXT
    ); 
    '''
    cur.execute(query)



def update_level(level, user_id):
    cur.execute('UPDATE users SET level = ? WHERE user_id = ?;', (level, user_id))

    con.commit()


def update_task(task, user_id):
    cur.execute('UPDATE users SET task = ? WHERE user_id = ?;', (task, user_id))

    con.commit()

def update_answer(answer, user_id):
    cur.execute('UPDATE users SET answer = ? WHERE user_id = ?;', (answer, user_id))

    con.commit()


def record_data(user_id, subject):
    cur.execute(
        '''INSERT or REPLACE INTO users (user_id, subject) VALUES(?, ?);''',
        (user_id, subject)
    )

    con.commit()


def select_data(user_id):
    results = cur.execute(f'''
    SELECT subject FROM
    users
    WHERE
    user_id = "{user_id}"
    LIMIT 1;
    ''')
    for res in results:
        print(res)