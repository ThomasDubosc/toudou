from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import logging

auth = HTTPBasicAuth()
users = {
    'john': generate_password_hash('hello'),
    'susan': generate_password_hash('bye')
}

@auth.verify_password
def verify_password(username, password):
    logging.info("**************************************************")
    if username in users and check_password_hash(users.get(username), password):
        return username
