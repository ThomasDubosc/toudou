import os

from flask import Flask, render_template, redirect, url_for, request, Blueprint, abort, flash
from datetime import datetime

from werkzeug.utils import secure_filename

import toudou.models as models
import toudou.services as services
from toudou import config

crud = Blueprint('crud', __name__, template_folder='templates',
    static_folder='static', static_url_path='/', url_prefix = '/')


UPLOAD_FOLDER = config['UPLOAD_FOLDER']

@crud.errorhandler(500)
def handle_internal_error(error):
    flash("Erreur interne du serveur", 'error')
    return redirect(url_for('crud.index'))

@crud.errorhandler(404)
def handle_internal_error(error):
    flash("La tache n'a pas été trouvée", 'error')
    return redirect(url_for('crud.index'))

@crud.route('/')
def index():
    listTodos = models.get_todos()
    return render_template('index.html', todos=listTodos)

@crud.route('/delete/<int:id>')
def delete(id):
    models.delete_todo(id)
    return redirect(url_for('crud.index'))

@crud.route('/create', methods=('GET', 'POST'))
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

@crud.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
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
        if todo == None:
            abort(404)
        return render_template('edit.html', todo=todo)


@crud.route('/export.csv')
def export_csv():
    csv = services.export_to_csv()
    return csv, 200, {'Content-Type': 'text/csv; charset=utf-8'}

@crud.route('/import_csv', methods=('GET', 'POST'))
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
        return redirect(url_for('crud.index'))

    return render_template('import_csv.html')

@crud.route('/signup')
def signup():
    print("jhhvfu")
    return render_template('/auth/signup.html')
