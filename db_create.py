from views import db
from models import Task
from datetime import date

# create the database and the db table
db.create_all()

# insert data
# db.session.add(Task('Finish this tutorial', date(2019, 10, 31), 10, 1))
# db.session.add(Task('Finish Real Python', date(2019, 12, 31), 1, 1))

# commit changes
db.session.commit()



