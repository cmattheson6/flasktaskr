import os
import unittest
from project import app, db
from project._config import basedir
from project.models import Task, User

from tests.test_template import TestTemplate

TEST_DB = 'test.db'

class TestMain(TestTemplate):
    def test_404_error(self):
        response = self.app.get('/this/does/not/exist')
        self.assertEquals(response.status_code, 404)
        self.assertIn(b'Sorry. There\'s nothing here.', response.data)

    def test_500_error(self):
        bad_user = User(
            name='Jeremy',
            email='jeremy@realpython.com',
            password='django'
        )

        db.session.add(bad_user)
        db.session.commit()
        self.assertRaises(ValueError, self.login, 'Jeremy', 'django')
        try:
            response = self.login('Jeremy', 'django')
            self.assertEquals(response.status_code, 500)
        except ValueError:
            pass


if __name__ == '__main__':
    unittest.main()