#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template('base.html', content="Home Page")

if __name__ == "__main__":
    app.run()
