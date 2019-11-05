from fabric.connection import Connection
from invoke import task
import sys


with Connection('localhost') as conn:

    # @task
    def test(c):
        c.run("nosetests -v")

    def test2(c):
        # with settings(warn_only=True):
        result = c.run('nosetests -v', capture=True)
        if result.failed and not bool(input('Tests failed. Continue?')):
            sys.exit()
            print('Aborted at user request.')

    def freeze(c):
        c.run('pip freeze > requirements.txt')

    # @task
    def commit(c):
        message = input('Enter a git commit message: ')
        print(type(message))
        c.run(f'git add . && git commit -m "{message}"')

    # @task
    def push_git(c):
        c.run('git push origin master -v')

    def pull(c):
        c.run('git pull origin master -v')

    def push_heroku(c):
        c.run('git push heroku master -v')

    def heroku_test(c):
        c.run('heroku run nosetests -v')

    def rollback(c):
        c.run('heroku rollback -v')

    @task
    def prepare(c=conn):
        pull(c)
        test(c)
        freeze(c)
        commit(c)
        push_git(c)
        push_heroku(c)
        heroku_test(c)
