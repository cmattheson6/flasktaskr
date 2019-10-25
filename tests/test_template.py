# Import packages
import os
import unittest
from project import app, db, bcrypt
from project._config import basedir
from project.models import Task, User

# all helper functions for testing

class TestTemplate(unittest.TestCase):
    TEST_DB = 'test.db' # can change as necessary, but this will be a base db
    app = app
    db = db

    def setUp(self):
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, self.TEST_DB)
        self.app = app.test_client()
        self.db.create_all()


    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()


    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password), follow_redirects=True)


    def logout(self):
        return self.app.get('logout', follow_redirects=True)


    def register_user(self, name, email, password, confirm):
        return self.app.post(
            'register/',
            data=dict(name=name,
                      email=email,
                      password=password,
                      confirm=confirm),
            follow_redirects=True
        )


    def create_user(self, name, email, password):
        new_user = User(name=name,
                        email=email,
                        password=bcrypt.generate_password_hash(password))
        self.db.session.add(new_user)
        self.db.session.commit()


    def create_task(self):
        return self.app.post('add', data=dict(
            name='Go to the bank',
            due_date='10/08/2019',
            priority='1',
            status='1'
        ), follow_redirects=True)

    def create_admin_user(self):
        new_user = User(
            name='Superman',
            email='admin@realpython.com',
            password=bcrypt.generate_password_hash('allpowerful'),
            role='admin'
        )
        db.session.add(new_user)
        db.session.commit()
