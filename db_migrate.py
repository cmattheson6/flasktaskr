from views import db
from _config import DATABASE_PATH

import sqlite3
from datetime import datetime

with sqlite3.connect(DATABASE_PATH) as conn:
    cur = conn.cursor()

    cur.execute("""ALTER TABLE tasks RENAME to old_tasks""")

    db.create_all()

    cur.execute("""select name, due_date, priority, status from old_tasks order by task_id asc""")

    data = [(row[0], row[1], row[2], row[3], datetime.now(), 1) for row in cur.fetchall()]

    cur.executemany("""insert into tasks (name, due_date, priority, status, posted_date, user_id)
        values (?, ?, ?, ?, ?, ?)""", data)

    cur.execute("""drop table old_tasks""")