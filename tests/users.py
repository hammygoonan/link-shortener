#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for users module."""

from tests.base import BaseTestCase


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
