#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Models."""

from shortener import db


class User(db.Model):

    """User model."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    invite_code = db.Column(db.String)
    reset_code = db.Column(db.String)

    def __init__(self, email, password, invite_code=None, reset_code=None):
        """Initialise model."""
        self.email = email
        self.password = password
        self.invite_code = invite_code
        self.reset_code = reset_code


class Link(db.Model):

    """Link model."""

    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String)

    user = db.relationship('User')

    def __init__(self, url, user, status):
        """Initialise model."""
        self.url = url
        self.user = user
        self.status = status
