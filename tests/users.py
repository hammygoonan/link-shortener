#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for users module."""

from tests.base import BaseTestCase
from flask.ext.login import current_user


class UsersTestCase(BaseTestCase):

    """User test cases."""

    def test_login_page(self):
        """Test login page."""
        response = self.client.get('/users/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_page(self):
        """Test register page."""
        response = self.client.get('/users/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_forgot_password_page(self):
        """Test forgot password page."""
        response = self.client.get('/users/forgot_password',
                                   content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Forgot Password', response.data)

    def test_edit_page(self):
        """Test user edit page."""
        response = self.client.get('/users/edit', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit your details', response.data)

    def test_logout(self):
        """Test logout mechanism."""
        with self.client:
            self.client.post(
                '/users/login',
                data=dict(email="hammy@spiresoftware.com.au",
                          password="password"),
                follow_redirects=True
            )
            response = self.client.get('/users/logout', follow_redirects=True)
            # todo: change this to a flash message
            self.assertIn(b'Login', response.data)
            self.assertFalse(current_user.is_active())
