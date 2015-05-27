#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shortener import db


class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String)
	password = db.Column(db.String)

	def __init__(self, email, password):
		self.email = email
		self.password = password


class Link(db.Model):
	__tablename__ = "links"

	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	status = db.Column(db.String)

	user = db.relationship('User')

	def __init__(self, url, user, status):
		self.url = url
		self.user = user
		self.status = status
