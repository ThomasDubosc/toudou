from flask import Flask
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
import logging

auth = HTTPBasicAuth()
authToken = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}


users = {
    'john': {
        'password' : generate_password_hash('hello'),
        'roles' : [ 'admin', 'user']
    },
    'susan': {
        'password' : generate_password_hash('bye'),
        'roles' : [ 'user']
    }
}

@authToken.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]
    
@auth.verify_password
def verify_password(username, password):
    logging.debug(f"verify_password({username}, {password})")
    if username in users and check_password_hash(users.get(username).get('password'), password):
        return username
    
@auth.get_user_roles
def get_user_roles(user):
    logging.debug(f"get_user_roles({user})")
    return users.get(user).get('roles')

