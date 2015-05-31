#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""users/views.py: User views."""

from flask import render_template, Blueprint, request, flash, redirect,\
    url_for
from flask.ext.login import login_user, login_required, logout_user,\
    current_user
from shortener import db, bcrypt, random_str
from shortener.models import User, Invitation, ResetPassword
from datetime import datetime, timedelta

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
        if(
            not request.form.get('email') or
            not request.form.get('password') or
            not request.form.get('invite')
        ):
            flash('Please ensure you fill in all fields.')
            return render_template('register.html')
        else:
            invite = Invitation.query.filter_by(
                email=request.form['email']
            ).first()
            if invite and invite.code == request.form.get('invite'):
                db.session.add(
                    User(request.form['email'], request.form['password'])
                )
                db.session.commit()
                flash('Thanks for signing up! Please login below.')
                return redirect(url_for('users.login'))
            else:
                flash('Sorry, we don\'t have a invite that matches that email '
                      'address and invitation code.')

    return render_template('register.html')


@users_blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password route."""
    if request.method == "POST":
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Sorry, we don\'t have that email address in our system.')
            return render_template('forgot_password.html')
        else:
            code = random_str(25)
            expires = datetime.utcnow() + timedelta(hours=24)
            db.session.add(ResetPassword(user, code, expires))
            db.session.commit()
            flash('Your password has been reset, please check your email.')

    return render_template('forgot_password.html')


@users_blueprint.route('/reset_password/<path:path>', methods=['GET', 'POST'])
def reset_password(path):
    """Reset password route."""
    if request.method == "POST":
        password = request.form.get('password')
        user = request.form.get('user_id')
        if password and user:
            user = User.query.get(user)
            user.password = bcrypt.generate_password_hash(password)
            db.session.commit()
            flash('Your password has been updated. Please login below.')
            return redirect(url_for('users.login'))
        else:
            flash('Sorry, something\'s not right here. Did you enter and '
                  'email address?.')

    reset = ResetPassword.query.filter_by(code=path).first_or_404()
    # moke sure link not expired
    if reset.expires < datetime.utcnow():
        flash('That link has expired. Please reset your password again.')
        return redirect(url_for('users.forgot_password'))
    return render_template('reset_password.html', user=reset.user_id)


@users_blueprint.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """Edit user route."""
    if request.method == "POST":
        user = User.query.filter_by(email=request.form['email']).first()
        # if email is already taken
        if user and user.id != current_user.id:
            flash('That email address is already in use.')
        else:
            user = User.query.get(current_user.id)
            # update password if changed
            if request.form['password'] != '':
                user.password = bcrypt.generate_password_hash(
                    request.form['password']
                )
            # update email if changed
            if current_user.email != request.form['email']:
                user.email = request.form['email']
            db.session.commit()
            flash('Your details have been updated')
    return render_template('edit.html', user=current_user)
