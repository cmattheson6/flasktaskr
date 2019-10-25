import os
import unittest
from project import app, db, bcrypt
from project._config import basedir
from project.models import Task, User

from tests.test_template import TestTemplate

TEST_DB = 'test.db'

class TestUsers(TestTemplate):

    def test_login_functionality(self):
        response = self.app.get('/')

        # Test presence of login form on page
        self.assertEqual(response.status_code, 200,
                         msg='The login webpage did not properly load.')
        self.assertIn(b'Please login to access your task list', response.data,
                      msg='The login form is not present on the page.')

        # Ensure registered users can log in
        self.register_user(name='cmattheson', email='cmattheson@test.com', password='testing', confirm='testing')
        response = self.login(name='cmattheson', password='testing')
        self.assertIn(b'Welcome', response.data,
                      msg='Test user was not able to login.')

        # Ensure non-registered users can't login
        response = self.login(name='fakeuser', password='thisissofake')
        self.assertIn(b'Invalid username or password', response.data,
                      msg='Fake user was able to enter the site.')

    def test_default_user_role(self):

        db.session.add(
            User(
                'Johnny',
                'john@doe.com',
                'johnny'
            )
        )
        db.session.commit()

        users = db.session.query(User).all()
        print(users)
        for user in users:
            self.assertEquals(user.role, 'user',
                              msg='New users not provided the correct default role.')


    def test_register_functionality(self):
        # Confirm register form is on webpage
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200,
                         msg='Unable to access register page.')
        self.assertIn(b'Please register to access the task list.', response.data,
                      msg='Register form is not present on page.')

        # Ensure new users can register and that info is properly received by database
        response = self.register_user(
            'cmattheson', 'cmattheson@test.com', 'testing', 'testing')
        test = db.session.query(User).first()
        print(test.name, test.email, test.password)
        self.assertTrue(test.name == 'cmattheson' \
               and test.email == 'cmattheson@test.com' \
               and bcrypt.check_password_hash(test.password, 'testing'),
               msg='New user information did not pass properly to database.')

    # After data has been received by database, the proper notifications are sent back to user.
        self.assertIn(b'Thanks for registering. Please login to confirm.', response.data,
                      msg='Confirmation notification not received by user.')

    # Do not allow duplicate users to be created and notify user of that
        self.app.get('register/', follow_redirects=True)
        response = self.register_user(
            name='cmattheson', email='cmattheson@test.com', password='testing', confirm='testing'
        )
        self.assertIn(b'That username and/or email already exists', response.data,
                      msg='User allowed to register multiple times with same user information.')


    def test_logout_functionality(self):

        # Ensure users not logged in cannot logout
        response = self.logout()
        self.assertNotIn(b'Goodbye', response.data,
                         msg='Users not logged in can access logout functionality.')

        # Ensure logged in users can logout
        self.register_user(name='cmattheson', email='cmattheson@test.com', password='testing', confirm='testing')
        self.login('cmattheson', 'testing')
        response = self.logout()
        self.assertIn(b'Goodbye', response.data,
                      msg='Users cannot logout.')

    def test_display_logged_in_username(self):
        self.register_user('cmattheson', 'cmattheson@test.com', 'testing', 'testing')
        self.login('cmattheson', 'testing')
        response = self.app.get('tasks', follow_redirects=True)
        self.assertIn(b'cmattheson', response.data)

if __name__ == '__main__':
    unittest.main()