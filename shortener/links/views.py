#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request

links_blueprint = Blueprint(
	'links', __name__,
	template_folder='templates'
)

@links_blueprint.route('/links', methods=['GET', 'POST'])
def list():
	""" Page with list of links and a form to add links """
	if request.method == "POST":
		pass

	return render_template('links.html')


@links_blueprint.route('/<path:path>')
def redirect(path):
	""" This is the big one """
	return path
