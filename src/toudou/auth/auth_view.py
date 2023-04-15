import os

from flask import Flask, render_template, redirect, url_for, request, Blueprint, abort, flash
from datetime import datetime

from werkzeug.utils import secure_filename

import toudou.models as models
import toudou.services as services
from toudou import config

auth = Blueprint('auth', __name__, template_folder='templates',
    static_folder='static', static_url_path='/', url_prefix = '/')


UPLOAD_FOLDER = config['UPLOAD_FOLDER']

