#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

from shortener.users.views import users_blueprint
from shortener.links.views import links_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(links_blueprint)

if __name__ == "__main__":
	app.run()
