#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.base import BaseTestCase

class UsersTestCase(BaseTestCase):
	"""User test cases."""

	def test_login_page(self):
		response = self.client.get('/users/login', content_type='html/text')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Login', response.data)

	def test_register_page(self):
		response = self.client.get('/users/register', content_type='html/text')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Login', response.data)

	def test_forgot_password_page(self):
		response = self.client.get('/users/forgot_password', content_type='html/text')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Forgot Password', response.data)
