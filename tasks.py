from fabric.connection import Connection
from invoke import task



with Connection('localhost') as conn:

    @task
    def test(c):
        c.run("nosetests -v")

    @task
    def commit(c):
        message = input('Enter a git commit message: ')
        c.run('git add . && git commit -am \'{}\''.format(message))

    @task
    def push(c):
        c.run('git push origin master')

    @task
    def prepare(c=conn):
        # test(c)
        commit(c)
        push(c)
