import os
import logging

from flask import Flask, render_template, redirect, url_for, request, Blueprint, jsonify
from datetime import date

from werkzeug.utils import secure_filename

import toudou.models as models
import toudou.services as services
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.types import String, Boolean, DateTime, BIGINT
from sqlalchemy import create_engine
from toudou.authy import authToken

from pydantic import BaseModel
from typing import Optional
from flask_pydantic import validate

api = Blueprint('api', __name__, static_url_path='/', url_prefix = '/api/todos')


class QueryParams(BaseModel):
  complete: Optional[bool]

@api.route('', methods=['GET'])
@authToken.login_required
@validate()
def list(query:QueryParams):
    if query.complete == None:
        return jsonify(models.get_todos())
    else:
        return jsonify(models.get_todos_completed(query.complete))


@api.route('/<int:id>', methods=['GET'])
@authToken.login_required
def get(id):
    todo = models.get_todo(id)
    if todo == None:
        return '', 404
    return jsonify(todo)

@api.route('/<int:id>', methods=['DELETE'])
@authToken.login_required
# ex: curl -X DELETE http://127.0.0.1:5000/api/toudou/925753
def delete(id):
    todo = models.get_todo(id)
    if todo:
        models.delete_todo(id)
        return '', 204
    return '', 404

class CreateData(BaseModel):
    task: str
    complete: Optional[bool]
    due: Optional[date]

@api.route('', methods=['POST'])
@authToken.login_required
@validate()
def create(body: CreateData):
    logging.info(body)
    id = models.create_todo(body.task, complete=body.complete, due=body.due)
    return jsonify(models.get_todo(id)), 201
    
class UpdateData(BaseModel):
    task: str
    complete: Optional[bool]
    due: Optional[date]

@api.route('/<int:id>', methods=['PUT'])
@authToken.login_required
@validate()
def update(id: int, body: UpdateData):
    logging.info(body)
    models.update_todo(id, body.task, body.complete, body.due)
    return jsonify(models.get_todo(id)), 200