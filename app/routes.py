from flask import request
from app import app
from fake_tasks.tasks import tasks_list
from datetime import datetime


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


@app.route("/tasks", methods=['POST'])
def create_task():
    if not request.is_json:
        return {'error':'Your content must be json'}, 400
    data = request.json
    required_fields = ['title', 'description']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error':f'{', '.join(missing_fields)} must be present'}
    title = data['title']
    description = data['description']
    new_task = {
        "id": len(tasks_list) + 1,
        "title": title,
        "description": description,
        "completed": False,
        "createdat": '24/12/2024',
        "duedate": data.get('duedate')
    }

    tasks_list.append(new_task)


    return new_task, 201
