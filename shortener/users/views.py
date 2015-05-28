#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""users/views.py: User views."""

from flask import render_template, Blueprint, request, flash, redirect,\
    url_for
from shortener.models import User
from flask.ext.login import login_user, login_required, logout_user
from shortener import bcrypt

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Login route."""
    if request.method == "POST":
        user = User.query.filter_by(email=request.form['email']).first()
        if user is not None and bcrypt.check_password_hash(
            user.password, request.form['password']
        ):
            login_user(user)
            return redirect(url_for('links.list'))

        else:
            flash('Invalid username or password.')

    return render_template('login.html')


@users_blueprint.route('/logout')
@login_required
def logout():
    """Logout route."""
    logout_user()
    flash('You were logged out')
    return redirect(url_for('users.login'))


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """Register route."""
    if request.method == "POST":
        pass

    return render_template('register.html')


@users_blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password route."""
    if request.method == "POST":
        pass

    return render_template('forgot_password.html')


@users_blueprint.route('/edit', methods=['GET', 'POST'])
def edit():
    """Edit user route."""
    if request.method == "POST":
        pass

    return render_template('edit.html')
