import os
import unittest
from project import app, db
from project._config import basedir
from project.models import Task, User

from tests.test_template import TestTemplate

TEST_DB = 'test.db'

class TestUsers(TestTemplate):
    def mock_test(self):
        pass

    def test_accessing_tasks_page(self):
        # invalid access without login
        bad_response = self.app.get('tasks', follow_redirects=True)
        self.assertIn(b'You need to login first', bad_response.data)

        # valid login process to access tasks
        self.register_user(
            'cmattheson', 'cmattheson@test.com', 'testing', 'testing'
        )
        self.login('cmattheson', 'testing')
        response = self.app.get('tasks')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new task', response.data)

    def test_task_add_functionality(self):
        # Mock create user and task
        self.create_user('cmattheson', 'cmattheson@test.com', 'testing')
        self.login('cmattheson', 'testing')
        self.app.get('testing', follow_redirects=True)

        # Attempt to upload a task that causes an error
        response = self.app.post('add/', data=dict(
            name='Go to the bank',
            due_date='',
            priority='1',
            posted_date='02/05/2014',
            status='1'), follow_redirects=True)
        self.assertNotIn(b'New task was successfully posted', response.data)

        # Confirm that the task in error was not uploaded
        test_error = db.session.query(Task).first()
        self.assertTrue(test_error == None,
                        msg='Task with inaccurate data structure was uploaded.')

        # Create a successful task
        response = self.create_task()
        test = db.session.query(Task).first()
        self.assertTrue(
            test.name == str('Go to the bank'),
               msg='Test task information was not added to database.')
        self.assertIn(b'New task was successfully posted', response.data,
                      msg='User was not provided post confirmation.')

    def test_complete_functionality(self):
        self.create_user('cmattheson', 'cmattheson@test.com', 'testing')
        self.login('cmattheson', 'testing')
        self.app.get('tasks', follow_redirects=True)
        self.create_task()
        response = self.app.get('complete/1', follow_redirects=True)
        test = db.session.query(Task).first()
        self.assertTrue(
            test.status == 0,
               msg='This test\'s completion status was not changed properly in the database.')
        self.assertIn(b'This task was marked as complete', response.data,
                      msg='A notification of successful status change was not provided to user.')

    def test_delete_functionality(self):
        # add test task to database and confirm it is in there
        self.create_user('cmattheson', 'cmattheson@test.com', 'testing')
        self.login('cmattheson', 'testing')
        self.app.get('tasks', follow_redirects=True)
        self.create_task()
        test = db.session.query(Task).first()
        self.assertTrue(
            test.name == str('Go to the bank'),
               msg='Test task information was not added to database.')

        # Confirm the task has been deleted
        response = self.app.get('delete/1', follow_redirects=True)
        test = db.session.query(Task).first()
        self.assertTrue(test == None,
                        msg='New task information was not deleted in database.')

        # Confirm the user is receiving a notification of the deletion.
        self.assertIn(b'This task has been successfully deleted', response.data,
                      msg='Notification of deletion not displayed correctly to user.')


    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()

        self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
        self.login('Fletcher', 'python101')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertNotIn(
            b'This task was marked as complete', response.data)
        self.assertIn(
            b'You can only update tasks that belong to you', response.data,
            msg='User was not provided error notification.')

    def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()

        self.create_user('Fletcher', 'fletcher@realpython.com', 'python101')
        self.login('Fletcher', 'python101')
        self.app.get('tasks', follow_redirects=True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertNotIn(
            b'This task has been successfully deleted', response.data)
        self.assertIn(
            b'You can only delete tasks that belong to you', response.data,
            msg='User was not provided error notification.'
        )

    def test_admin_users_can_complete_all_tasks(self):
        self.create_user('cmattheson', 'cmattheson@test.com', 'testing')
        self.login('cmattheson', 'testing')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'allpowerful')
        self.app.get('tasks', follow_redirects=True)
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertNotIn(b'You can only update tasks that belong to you', response.data)

    def test_admin_users_can_delete_all_tasks(self):
        self.create_user('cmattheson', 'cmattheson@test.com', 'testing')
        self.login('cmattheson', 'testing')
        self.app.get('tasks', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'allpowerful')
        self.app.get('tasks', follow_redirects=True)
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertNotIn(b'You can only delete tasks that belong to you', response.data)

    def test_visibility_of_links_functionality(self):
        # Test that links you create are visibile for you
        self.create_user('cmattheson', 'cmattheson@test.com', 'testing')
        self.login('cmattheson', 'testing')
        self.app.get('tasks', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'/complete/1/', response.data,
                      msg = 'User cannot view modification links for their tasks.')
        self.assertIn(b'/delete/1/', response.data,
                      msg = 'User cannot view modification links for their tasks.')

        # Test that links not created by you are not visible
        self.create_user('randomuser', 'random@test.com', 'thisisntreal')
        self.login('randomuser', 'thisisntreal')
        response = self.app.get('tasks', follow_redirects=True)
        self.assertNotIn(b'/complete', response.data,
                      msg = 'User can view modification links for others\' tasks.')
        self.assertNotIn(b'/delete', response.data,
                      msg = 'User can view modification links for others\' tasks.')

        # Test that admins have access to everything
        self.create_admin_user()
        self.login('Superman', 'allpowerful')
        response = self.app.get('tasks', follow_redirects=True)
        self.assertIn(b'/complete/1/', response.data,
                      msg = 'Admin cannot view modification links for their tasks.')
        self.assertIn(b'/delete/1/', response.data,
                      msg = 'Admin cannot view modification links for their tasks.')


if __name__ == '__main__':
    unittest.main()