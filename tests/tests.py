# import os
# import unittest
#
# from views import app, db
# from _config import basedir
# from models import User
#
# TEST_DB = 'test.db'
#
# class AllTests(unittest.TestCase):
#     # Test setup and cleanup
#     def setUp(self):
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
#         self.app = app.test_client()
#         db.create_all()
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#
#     # all helper functions for testing
#
#     def login(self, name, password):
#         return self.app.post('/', data=dict(
#             name=name, password=password), follow_redirects=True)
#
#     def logout(self):
#         return self.app.get('logout', follow_redirects=True)
#
#     def register_user(self, name, email, password, confirm):
#         return self.app.post(
#             'register/',
#             data=dict(name=name,
#                       email=email,
#                       password=password,
#                       confirm=confirm),
#             follow_redirects=True
#         )
#
#     def create_user(self, name, email, password):
#         new_user = User(name=name, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#
#     def create_task(self):
#         return self.app.post('add', data=dict(
#             name='Go to the bank',
#             due_date='10/08/2019',
#             priority='1',
#             posted_date='10/08/2019',
#             status='1'
#         ), follow_redirects=True)
#
#     # Tests go below
#
#     def test_users_can_register(self):
#         new_user = User('michael', 'michael@test.org', 'password')
#         db.session.add(new_user)
#         db.session.commit()
#         test = db.session.query(User).all()
#         for t in test:
#             t.name
#         assert t.name == 'michael'
#
#     def test_form_is_present(self):
#         response = self.app.get('/')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'Please sign in to access your task list', response.data)
#
#
#     def test_users_cannot_login_unless_registered(self):
#         response = self.login('foo', 'bar')
#         self.assertIn(b'Invalid username or password', response.data)
#
#     def test_users_can_login(self):
#         self.register_user('Michael', 'michael@realpython', 'python', 'python')
#         response = self.login('Michael', 'python')
#         self.assertIn(b'Welcome', response.data)
#
#     def test_invalid_user_data(self):
#         self.register_user('Michael', 'michael@realpython', 'python', 'python')
#         response = self.login('alert("Alert box!");', 'bar')
#         self.assertIn(b'Welcome', response.data)
#
#     def test_form_is_present_on_register_page(self):
#         response = self.app.get('register/')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'Please register to access the task list.', response.data)
#
#     def test_user_registration(self):
#         self.app.get('register/', follow_redirects=True)
#         response = self.register_user(
#             'Michael', 'michael@realpython.com', 'python', 'python'
#         )
#         self.assertIn(b'Thanks for registering. Please login to confirm.', response.data)
#
#     def test_user_registration_error(self):
#         self.app.get('register/', follow_redirects=True)
#         response = self.register_user(
#             'Michael', 'michael@realpython.com', 'python', 'python'
#         )
#         self.app.get('register/', follow_redirects=True)
#         response = self.register_user(
#             'Michael', 'michael@realpython.com', 'python', 'python'
#         )
#         self.assertIn(b'That username and/or email already exists', response.data)
#
#     def test_logged_in_users_can_logout(self):
#         self.register_user('Fletcher', 'fletcher@realpython.com', 'python', 'python')
#         self.login('Fletcher', 'python')
#         response = self.logout()
#         self.assertIn(b'Goodbye', response.data)
#
#     def test_not_logged_in_users_cannot_logout(self):
#         response = self.logout()
#         self.assertNotIn(b'Goodbye', response.data)
#
#     def test_accessing_tasks_page(self):
#         # invalid access without login
#         bad_response = self.app.get('tasks', follow_redirects=True)
#         self.assertIn(b'You need to login first', bad_response.data)
#
#         # valid login process to access tasks
#         self.register_user(
#             'Fletcher', 'fletcher@realpython.com', 'python', 'python'
#         )
#         self.login('Fletcher', 'python')
#         response = self.app.get('tasks')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'Add a new task', response.data)
#
#     def test_user_can_add_tasks(self):
#         self.create_user('Michael', 'michael@realpython.com', 'python')
#         self.login('Michael', 'python')
#         self.app.get('tasks', follow_redirects=True)
#         response = self.create_task()
#         self.assertIn(b'New task was successfully posted', response.data)
#
#     def test_users_cannot_add_task_when_error(self):
#         self.create_user('Michael', 'michael@realpython.com', 'python')
#         self.login('Michael', 'python')
#         self.app.get('tasks', follow_redirects=True)
#         response = self.app.post('add/', data=dict(
#             name='Go to the bank',
#             due_date='',
#             priority='1',
#             posted_date='02/05/2014',
#             status='1'), follow_redirects=True)
#         self.assertNotIn(b'New task was successfully posted', response.data)
#
#     def test_users_can_complete_tasks(self):
#         self.create_user('Michael', 'michael@realpython.com', 'python')
#         self.login('Michael', 'python')
#         self.app.get('tasks', follow_redirects=True)
#         self.create_task()
#         response = self.app.get('complete/1', follow_redirects=True)
#         self.assertIn(b'This task was marked as complete', response.data)
#
#     def test_users_can_delete_tasks(self):
#         self.create_user('Michael', 'michael@realpython.com', 'python')
#         self.login('Michael', 'python')
#         self.app.get('tasks', follow_redirects=True)
#         self.create_task()
#         response = self.app.get('delete/1', follow_redirects=True)
#         self.assertIn(b'This task has been successfully deleted', response.data)
#
#     def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
#         self.create_user('Michael', 'michael@realpython.com', 'python')
#         self.login('Michael', 'python')
#         self.app.get('tasks/', follow_redirects=True)
#         self.create_task()
#         self.logout()
#
#         self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
#         self.login('Fletcher', 'python101')
#         self.app.get('tasks/', follow_redirects=True)
#         response = self.app.get("complete/1/", follow_redirects=True)
#         self.assertNotIn(
#             b'This task was marked as complete', response.data)
#
#
# if __name__ == '__main__':
#     unittest.main()
