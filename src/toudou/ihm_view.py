import os
import logging

from flask import Flask, render_template, redirect, url_for, request, Blueprint, abort, flash
from datetime import datetime

from werkzeug.utils import secure_filename

import toudou.models as models
import toudou.services as services
from toudou import config

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField
from wtforms.validators import DataRequired, Optional
from toudou.authy import auth

ihm = Blueprint('ihm', __name__, template_folder='templates',
    static_folder='static')

UPLOAD_FOLDER = config['UPLOAD_FOLDER']

@ihm.errorhandler(500)
def handle_internal_error(error):
    logging.exception(error)
    flash("Erreur interne du serveur", 'error')
    return redirect(url_for('ihm.index'))

@ihm.errorhandler(404)
def handle_internal_error(error):
    logging.exception(error)
    flash("La tache n'a pas été trouvée", 'error')
    return redirect(url_for('ihm.index'))


@ihm.route('/')
@auth.login_required(role=['admin', 'user'])
def index():
    listTodos = models.get_todos()
    return render_template('index.html', todos=listTodos, username=auth.username())

@ihm.route('/delete/<int:id>')
@auth.login_required(role='admin')
def delete(id):
    models.delete_todo(id)
    return redirect(url_for('ihm.index'))

class CreateForm(FlaskForm):
    task = StringField('task', validators=[DataRequired()])
    complete = BooleanField('')
    due = DateField('', format='%Y-%m-%d', validators=[Optional()])

@ihm.route('/create', methods=('GET', 'POST'))
@auth.login_required(role='admin')
def create():
    form = CreateForm()
    if request.method == 'POST':
        logging.info(f"-----------------Creation d'une nouvelle tache: {form.task.data}" )

        if form.validate_on_submit():
            models.create_todo(form.task.data, complete=form.complete.data, due=form.due.data)
            return redirect(url_for('ihm.index'))

        return render_template('create.html', form=form)

    return render_template('create.html', form=form)

@ihm.route('/edit/<int:id>', methods=('GET', 'POST'))
@auth.login_required(role='admin')
def edit(id):
    if request.method == 'POST':
        logging.info(f"Mise à jour de la tache {id}")
        task = request.form['task']

        complete = False
        if request.form.get('complete'):
            complete = bool(request.form.get('complete'))

        dueString = request.form['due']
        due = None
        if dueString:
            due = datetime.strptime(dueString, '%Y-%m-%d')

        models.update_todo(id, task, complete, due)
        return redirect(url_for('ihm.index'))

    else:
        todo = models.get_todo(id)
        if todo == None:
            abort(404)
        return render_template('edit.html', todo=todo)


@ihm.route('/export.csv')
@auth.login_required
def export_csv():
    csv = services.export_to_csv()
    return csv, 200, {'Content-Type': 'text/csv; charset=utf-8'}

@ihm.route('/import_csv', methods=('GET', 'POST'))
@auth.login_required(role='admin')
def import_csv():

    if request.method == 'POST':
        # upload file flask
        uploaded_df = request.files['file']

        # Extracting uploaded data file name
        data_filename = secure_filename(uploaded_df.filename)

        # flask upload file to database (defined uploaded folder in static path)
        uploaded_df.save(os.path.join(UPLOAD_FOLDER, data_filename))

        fileOnDisk = os.path.join(UPLOAD_FOLDER, data_filename)
        fp = open(fileOnDisk, mode="r", encoding="utf-8")
        csv = fp.read()
        fp.close()
        services.import_from_csv(csv)
        return redirect(url_for('ihm.index'))

    return render_template('import_csv.html')

@ihm.route('/signup')
def signup():
    print("jhhvfu")
    return render_template('/auth/signup.html')
