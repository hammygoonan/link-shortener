#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""links/views.py: Links views."""


from flask import render_template, Blueprint, request, redirect, url_for
from flask.ext.login import login_required, current_user
from shortener.models import Link

links_blueprint = Blueprint(
    'links', __name__,
    template_folder='templates'
)


@links_blueprint.route('/list')
@login_required
def list():
    """Page with list of links."""
    links = Link.query.filter_by(user_id=current_user.id).all()
    return render_template('links.html', links=links)


@links_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """Page with list of links and a form to add links."""
    if request.method == "POST":
        pass

    return render_template('add.html')

@links_blueprint.route('/')
def home():
    """Redirector, and logger of links."""
    return redirect(url_for('users.login'))


@links_blueprint.route('/<path:path>')
def redirect_link(path):
    """Redirector, and logger of links."""
    return path
