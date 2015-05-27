#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module init file. Runs application."""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager


app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

from shortener.users.views import users_blueprint
from shortener.links.views import links_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(links_blueprint)


from shortener.models import User

login_manager.login_view = "users.login"
login_manager.login_message = "Please login to view that page."


@login_manager.user_loader
def load_user(user_id):
    """Load the logged in user for the LoginManager."""
    return User.query.filter(User.id == int(user_id)).first()
