#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request

users_blueprint = Blueprint(
	'users', __name__,
	template_folder='templates'
)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		pass

	return render_template('login.html')


@users_blueprint.route('/logout')
def logout():
	pass

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == "POST":
		pass

	return render_template('login.html')

@users_blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
	if request.method == "POST":
		pass

	return render_template('forgot_password.html')