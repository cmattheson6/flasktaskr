from views import db
from _config import DATABASE_PATH

import sqlite3
from datetime import datetime

def migrate_tasks():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cur = conn.cursor()

        cur.execute("""ALTER TABLE tasks RENAME to old_tasks""")

        db.create_all()

        cur.execute("""select name, due_date, priority, status from old_tasks order by task_id asc""")

        data = [(row[0], row[1], row[2], row[3], datetime.now(), 1) for row in cur.fetchall()]

        cur.executemany("""insert into tasks (name, due_date, priority, status, posted_date, user_id)
            values (?, ?, ?, ?, ?, ?)""", data)

        cur.execute("""drop table old_tasks""")

def migrate_users():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cur = conn.cursor()

        cur.execute("""ALTER TABLE users RENAME to old_users""")

        db.create_all()

        cur.execute("""select name, email, password from old_users order by id asc""")

        data = [(row[0], row[1], row[2], 'user') for row in cur.fetchall()]

        cur.executemany("""insert into users (name, email, password, role)
            values (?, ?, ?, ?)""", data)

        cur.execute("""drop table old_users""")

if __name__ == '__main__':
    tbl_name = input('What table would you like to update? \nModel Class Name:')

    if tbl_name == 'User':
        migrate_users()
    elif tbl_name == 'Task':
        migrate_tasks()
    else:
        raise ValueError('This model class does not exist.')