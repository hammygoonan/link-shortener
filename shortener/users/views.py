#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""User views."""

from flask import render_template, Blueprint, request

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Login route."""
    if request.method == "POST":
        pass

    return render_template('login.html')


@users_blueprint.route('/logout')
def logout():
    """Logout route."""
    pass


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """Register route."""
    if request.method == "POST":
        pass

    return render_template('login.html')


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
