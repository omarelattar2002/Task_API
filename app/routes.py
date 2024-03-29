from flask import request
from app import app
from fake_tasks.tasks import tasks_list


@app.route("/")
def index():
    return "This is the Tasks API page"

@app.route("/tasks")
def show_tasks():
    return tasks_list


@app.route("/tasks/<int:task_id>")
def get_tasks(task_id):
    for task in tasks_list:
        if task['id'] == task_id:
            return task
    return {'error':f'The ID{task_id} does not exist'}, 404
    