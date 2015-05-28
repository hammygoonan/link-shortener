#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for users module."""

from tests.base import BaseTestCase
from flask.ext.login import current_user
from shortener import app
from flask import url_for


class UsersTestCase(BaseTestCase):

    """User test cases."""

    def test_login_page(self):
        """Test login page."""
        response = self.client.get('/users/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_can_login(self):
        """Test user can login."""
        with self.client:
            response = self.client.post(
                url_for('users.login'),
                follow_redirects=True,
                data={
                    'email': 'hammy@spiresoftware.com.au',
                    'password': 'password'
                },
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Link', response.data)
            self.assertTrue(current_user.is_active())
            self.assertTrue(current_user.email == 'hammy@spiresoftware.com.au')

    def test_cant_login(self):
        """Test that can't login with incorrect details and flash message."""
        with self.client:
            response = self.client.post(
                '/users/login',
                follow_redirects=True,
                data=dict(
                    email='hammy1@spiresoftware.com.au',
                    password='123'
                ),
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Invalid username or password.', response.data)
            self.assertFalse(current_user.is_active())

    def test_register_page(self):
        """Test register page."""
        response = self.client.get('/users/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_forgot_password_page(self):
        """Test forgot password page."""
        response = self.client.get('/users/forgot_password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Forgot Password', response.data)

    def test_edit_page(self):
        """Test user edit page."""
        response = self.client.get('/users/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit your details', response.data)

    def test_logout(self):
        with self.client:
            self.client.post(
                '/users/login',
                data=dict(username="hammy@spiresoftware.com.au",
                          password="password"),
                follow_redirects=True
            )
            response = self.client.get('/users/logout', follow_redirects=True)
            self.assertIn(b'You were logged out', response.data)
            self.assertFalse(current_user.is_active())

    # Ensure that logout page requires user login
    def test_logout_route_requires_login(self):
        response = self.client.get('/users/logout', follow_redirects=True)
        self.assertIn(b'Please login to view that page.', response.data)

    # def test_logout(self):
    #     """Test logout mechanism."""
    #     with self.client:
    #         response = self.client.post(
    #             '/users/login',
    #             data=dict(email="hammy@spiresoftware.com.au",
    #                       password="password"),
    #             follow_redirects=True
    #         )
    #         self.assertIn(b'You were logged out', response.data)
