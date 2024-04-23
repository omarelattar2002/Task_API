from flask import request
from app import app
from app.models import Task, User
from fake_tasks.tasks import tasks_list
from datetime import datetime
from . import db
from flask import jsonify
from app.auth import basic_auth, token_auth

@app.route("/")
def index():
    return "This is the Tasks API page"

@app.route("/tasks")
def show_tasks():
    return jsonify(json_list=[task.to_json for task in Task.query.all()])



@app.route("/tasks/<int:task_id>")
def get_tasks(task_id):
    task = Task.query.get(task_id)
    if not task:
        return {'error':f'The task with ID {task_id} does not exist'}, 404
    return jsonify(task.to_json), 200


@app.route("/tasks", methods=['POST'])
@token_auth.login_required
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
        return {'error': f"{','.join(missing_fields)} must be in the request body"}, 400
    title = data['title']
    description = data['description']
    current_user = token_auth.current_user()
    new_task = Task(title=title, description=description, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return new_task.to_json, 201

@app.route("/tasks/<int:task_id>", methods=['PUT'])
@token_auth.login_required
def update_task(task_id):
    Task.query.filter_by(id=task_id).update({'completed': True})
    db.session.commit()
    return {'message':f'Task {task_id} has been completed'}, 200


@app.route("/tasks/<int:task_id>", methods=['DELETE'])
@token_auth.login_required
def delete_task(task_id):
    Task.query.filter_by(id=task_id).delete()
    db.session.commit()
    return {'message':f'Task {task_id} has been deleted'}, 200


@app.route("/users", methods=['POST'])
def create_user():
    if not request.is_json:
        return {'error':'Your content must be json'}, 400
    data = request.json
    required_fields = ['username', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    username = data['username']
    email = data['email']
    password = data['password']
    new_user = User(username=username, email=email, password_hash=hash(password))
    return new_user.to_json, 201


@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {'error':f'The user with ID {user_id} does not exist'}, 404
    return jsonify(user.to_json), 200

@app.route("/users/<int:user_id>", methods=['PUT'])
@token_auth.login_required
def update_user(user_id):
    if not request.is_json:
        return {'error':'Your content must be json'}, 400
    user = User.query.get(user_id)
    if not user:
        return {'error':f'The user with ID {user_id} does not exist'}, 404
    return user
    
@app.route('/users/<int:user_id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {'error':f'The user with ID {user_id} does not exist'}, 404
    db.session.delete(user)
    db.session.commit()
    return {'message':f'User {user_id} has been deleted'}, 200


@app.route('/token')
@basic_auth.login_required
def create_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return jsonify({'token': token.get("token").decode('utf-8'),"token-expiration":token.get("token_expiration")}), 200
