from flask import Flask, jsonify
from functools import wraps
from flask_restful import Resource, Api, reqparse
from flask_restful.inputs import date as inputs_date
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime

from project import db
from project.models import Task

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('due_date', type=inputs_date)
parser.add_argument('priority', type=int)
parser.add_argument('posted_date', type=inputs_date)
parser.add_argument('status', type=int)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.resource('/tasks')
class AllTasks(Resource):
    def get(self):
        results = db.session.query(Task).limit(10).offset(0).all()
        json_results = []
        for result in results:
            data = {
                'task_id': result.task_id,
                'task_name': result.name,
                'due_date': str(result.due_date),
                'priority': result.priority,
                'posted_date': str(result.posted_date),
                'status': result.status,
                'user_id': result.user_id
            }
            json_results.append(data)
        return jsonify(items=json_results)


@api.resource('/tasks/add')
class AddTasks(Resource):

    def post(self):
        args = parser.parse_args()
        print(args['name'])
        print(args['priority'])
        print(args['due_date'])

        new_task = Task(
            args['name'],
            args['due_date'],
            args['priority'],
            datetime.datetime.utcnow(),
            1,
            1)
        db.session.add(new_task)
        db.session.commit()
        name = args['name']
        data = {
            'msg': f'Your task \'{name}\' has been posted as task 2.'
        }

        return jsonify(data)

# @api.add_resource('/task')
class TaskItem(Resource):
    def get(self, task_id):
        result = db.session.query(Task).filter_by(task_id=task_id).first()
        data = {
            'task_id': result.task_id,
            'name': result.name,
            'due_date': str(result.due_date),
            'priority': result.priority,
            'posted_date': str(result.posted_date),
            'status': result.status,
            'user_id': result.user_id
        }

        return jsonify(data)

    def put(self, task_id):
        args = parser.parse_args()
        print(args)
        args = {k: v for k, v in args.items() if v is not None}
        task = db.session.query(Task).filter_by(task_id=task_id)
        task.update(args)
        db.session.commit()

        data = {
            'msg': f'Your task has been updated.'
        }

        return jsonify(data)

    def delete(self, task_id):
        db.session.query(Task).filter_by(task_id=task_id).delete()
        db.session.commit()
        data = {
            'msg': f'Your task number {task_id} has been deleted.'
        }

        return jsonify(data)

api.add_resource(TaskItem, '/tasks/<int:task_id>')

#
# def login_required(test):
#     @wraps(test)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return test(*args, **kwargs)
#         else:
#             flash('You need to login first.')
#             return redirect(url_for('users.login'))
#     return wrap
#
# # route handlers
#
#
# # Opening and closing task SQLAlchemy fxns
#
# def open_tasks():
#     return db.session.query(Task).filter_by(
#         status='1').order_by(Task.due_date.asc())
#
# def closed_tasks():
#     return db.session.query(Task).filter_by(
#         status='0').order_by(Task.due_date.asc())
#
# @tasks_blueprint.route('/tasks')
# @login_required
# def tasks():
#     return render_template(
#         'tasks.html',
#         form=AddTaskForm(request.form),
#         open_tasks=open_tasks(),
#         closed_tasks=closed_tasks(),
#         username=session['name']
#     )
#
# @tasks_blueprint.route('/add/', methods=['GET', 'POST'])
# @login_required
# def new_task():
#     error = None
#     form = AddTaskForm(request.form)
#     if request.method=='POST':
#         if form.validate_on_submit():
#             new_task = Task(
#                 form.name.data,
#                 form.due_date.data,
#                 form.priority.data,
#                 datetime.datetime.utcnow(),
#                 '1',
#                 session['user_id']
#             )
#             db.session.add(new_task)
#             db.session.commit()
#             flash('New task was successfully posted.')
#         else:
#             return redirect(url_for('tasks.tasks'))
#         return render_template('tasks.html',
#                                form=form,
#                                error=error,
#                                open_tasks=open_tasks(),
#                                closed_tasks=closed_tasks())
#
# @tasks_blueprint.route('/complete/<int:task_id>/')
# @login_required
# def complete(task_id):
#     new_id = task_id
#     task = db.session.query(Task).filter_by(task_id=new_id)
#     if session['role'] == 'admin' or session['user_id'] == task.first().user_id:
#         task.update({'status': '0'})
#         db.session.commit()
#         flash('This task was marked as complete.')
#     else:
#         flash('You can only update tasks that belong to you.')
#     return redirect(url_for('tasks.tasks'))
#
# @tasks_blueprint.route('/delete/<int:task_id>/')
# @login_required
# def delete_entry(task_id):
#     new_id = task_id
#     task = db.session.query(Task).filter_by(task_id=new_id)
#     if session['role'] == 'admin' or session['user_id'] == task.first().user_id:
#         task.delete()
#         db.session.commit()
#         flash('This task has been successfully deleted')
#     else:
#         flash('You can only delete tasks that belong to you.')
#     return redirect(url_for('tasks.tasks'))
#
#
# api.add_resource(HelloWorld, '/')
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#






if __name__ == '__main__':
    app.run(debug=True)

def fake():
    print('This is totally not a correct function')
    x = 'Making a change to test Travis CI'
    print(x)