#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""links/views.py: Links views."""


import re
from flask import render_template, Blueprint, request, redirect, url_for,\
    flash
from flask.ext.login import login_required, current_user
from shortener import app, db, random_str
from shortener.models import Link
from datetime import datetime

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
    link = None
    if request.method == "POST":
        url = request.form.get('url')
        if not url:
            flash('Forget to add a link?')
            return render_template('add.html')
        # validate url with Django url checker
        url_regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|'
            r'[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not re.match(url_regex, url):
            flash('That link isn\'t formatted correctly.')
            return render_template('add.html')

        # check if that user has already saved this link
        pre_existing = Link.query.filter_by(
            user_id=current_user.id, url=url).first()
        if pre_existing:
            flash('{} - has been added previously.'.format(url))
            link = pre_existing
        else:
            # get unique slug
            unique_slug = None
            while not unique_slug:
                # (26 + 26 + 10) ** 4 =  14,776,336 - that's unique enough
                slug = random_str(4)
                if not Link.query.filter_by(slug=slug).first():
                    unique_slug = slug

            # add link
            link = Link(url, slug, current_user)
            db.session.add(link)
            db.session.commit()
            flash('Your link was added - {}.'.format(url))

    return render_template('add.html', link=link)


@links_blueprint.route('/')
def home():
    """Redirector, and logger of links."""
    if current_user.is_authenticated():
        return redirect(url_for('links.add'))
    return redirect(url_for('users.login'))


@links_blueprint.route('/<path:path>')
def redirect_link(path):
    """Redirector, and logger of links."""
    link = Link.query.filter_by(slug=path).first_or_404()
    log_entry = '{}\t{}\t{}\t{}\n'.format(
        datetime.now(), link.url, request.remote_addr,
        request.headers.get('User-Agent'))

    with open(app.config.get('LOG_FILE'), 'a') as f:
        f.write(log_entry)
    return redirect(link.url)
