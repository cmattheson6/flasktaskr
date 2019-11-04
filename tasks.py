from fabric.connection import Connection
from invoke import task



with Connection('localhost') as conn:

    @task
    def test(c):
        c.run("nosetests -v")

    @task
    def commit(c):
        message = input('Enter a git commit message: ')
        print(type(message))
        c.run(f'git add . && git commit -m "{message}"')#.format(message))

    @task
    def push(c):
        c.run('git push origin master -v')

    @task
    def prepare(c=conn):
        test(c)
        commit(c)
        push(c)
