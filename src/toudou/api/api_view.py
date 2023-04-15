import os

from flask import Flask, render_template, redirect, url_for, request, Blueprint, jsonify
from datetime import datetime

from werkzeug.utils import secure_filename

import toudou.models as models
import toudou.services as services
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.types import String, Boolean, DateTime, BIGINT
from sqlalchemy import create_engine

api = Blueprint('api', __name__, static_url_path='/', url_prefix = '/api/toudou')


@api.route('/', methods=['GET'])
def list():
    with Session(models.engine) as session:
        return jsonify(session.query(models.Todo).all())

@api.route('/<int:id>', methods=['GET'])
def get(id):
    # rechercher mon objet Toudou
    with Session(models.engine) as session:
        return jsonify(session.query(models.Todo).get(id))

@api.route('/<int:id>', methods=['DELETE'])
# ex: curl -X DELETE http://127.0.0.1:5000/api/toudou/925753
def delete(id):
    todo = models.get_todo(id)
    if todo:
        with Session(models.engine) as session:
            session.delete(todo)
            session.commit()
        return '', 204
    return '', 404



@api.route('/', methods=['POST'])
def create():
    if request.method == 'POST':
        task = request.form['task']

        complete = False
        if request.form.get('complete'):
            complete = bool(request.form.get('complete'))

        dueString = request.form['due']
        due = None
        if dueString:
            due = datetime.strptime(dueString, '%Y-%m-%d')

        models.create_todo(task, complete=complete, due=due)
        return redirect(url_for('crud.index'))
    return render_template('create.html')

@api.route('/<int:id>', methods=['PUT'])
def update(id):
    if request.method == 'POST':
        task = request.form['task']

        complete = False
        if request.form.get('complete'):
            complete = bool(request.form.get('complete'))

        dueString = request.form['due']
        due = None
        if dueString:
            due = datetime.strptime(dueString, '%Y-%m-%d')

        models.update_todo(id, task, complete, due)
        return redirect(url_for('crud.index'))

    else:
        todo = models.get_todo(id)
        return render_template('edit.html', todo=todo)
