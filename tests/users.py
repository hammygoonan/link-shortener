#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for users module."""

from tests.base import BaseTestCase
from flask.ext.login import current_user
from shortener import bcrypt
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
        with self.client:
            self.client.post(
                '/users/login',
                data={
                    'email': 'hammy@spiresoftware.com.au',
                    'password': 'password'
                },
                follow_redirects=True
            )
            response = self.client.get('/users/edit')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Edit your details', response.data)

    def test_logout(self):
        """Test user can logout."""
        with self.client:
            response = self.client.post(
                '/users/login',
                data={
                    'email': 'hammy@spiresoftware.com.au',
                    'password': 'password'
                },
                follow_redirects=True
            )
            response = self.client.get('/users/logout', follow_redirects=True)
            self.assertIn(b'You were logged out', response.data)
            self.assertFalse(current_user.is_active())

    def test_logout_route_requires_login(self):
        """Ensure that logout page requires user login."""
        response = self.client.get('/users/logout', follow_redirects=True)
        self.assertIn(b'Please login to view that page.', response.data)

    def test_user_can_change_email(self):
        """Test the user can update email."""
        with self.client:
            response = self.client.post(
                '/users/login',
                data={
                    'email': 'hammy@spiresoftware.com.au',
                    'password': 'password'
                },
                follow_redirects=True
            )
            self.assertTrue(current_user.email == 'hammy@spiresoftware.com.au')
            response = self.client.post(
                '/users/edit',
                data={
                    'email': 'hammy2@spiresoftware.com.au',
                    'password': ''
                },
                follow_redirects=True
            )
            # check email has been updated
            self.assertTrue(current_user.email ==
                            'hammy2@spiresoftware.com.au')
            # make sure password hasn't been updated
            password = bcrypt.check_password_hash(
                current_user.password, 'password'
            )
            self.assertTrue(password)
            # check flash message
            self.assertIn(b'Your details have been updated', response.data)

    def test_user_can_change_password(self):
        """Test that user can change password."""
        with self.client:
            response = self.client.post(
                '/users/login',
                data={
                    'email': 'hammy@spiresoftware.com.au',
                    'password': 'password'
                },
                follow_redirects=True
            )
            user_password = bcrypt.check_password_hash(
                current_user.password, 'password'
            )
            self.assertTrue(user_password)
            response = self.client.post(
                '/users/edit',
                data={
                    'email': 'hammy@spiresoftware.com.au',
                    'password': 'new_password'
                },
                follow_redirects=True
            )
            # check password is updated
            new_password = bcrypt.check_password_hash(
                current_user.password, 'new_password'
            )
            self.assertTrue(new_password)
            # check email remains the same
            self.assertTrue(current_user.email ==
                            'hammy@spiresoftware.com.au')
            # check flash message
            self.assertIn(b'Your details have been updated', response.data)

    def test_user_unique_when_editing(self):
        """Test that email being edited is unique and email is not updated."""
        with self.client:
            response = self.client.post(
                '/users/login',
                data={
                    'email': 'hammy@spiresoftware.com.au',
                    'password': 'password'
                },
                follow_redirects=True
            )
            self.assertTrue(current_user.email == 'hammy@spiresoftware.com.au')
            response = self.client.post(
                '/users/edit',
                data={
                    'email': 'test@spiresoftware.com.au',
                    'password': ''
                },
                follow_redirects=True
            )
            # check email has not been updated
            self.assertTrue(current_user.email ==
                            'hammy@spiresoftware.com.au')
            # display flash message
            self.assertIn(b'That email address is already in use.',
                          response.data)

    def test_user_cannt_register_without_all_fields(self):
        """Check all fields are required for user registration."""
        with self.client:
            # check invite required
            response = self.client.post(
                '/users/register',
                data={
                    'email': 'hammy2@spiresoftware.com.au',
                    'password': 'password',
                    'invite': ''
                },
                follow_redirects=True
            )
            self.assertIn(b'Please ensure you fill in all fields.',
                          response.data)
            # check password required
            response = self.client.post(
                '/users/register',
                data={
                    'email': 'hammy2@spiresoftware.com.au',
                    'password': '',
                    'invite': 'invite_code'
                },
                follow_redirects=True
            )
            self.assertIn(b'Please ensure you fill in all fields.',
                          response.data)
            # check email required
            response = self.client.post(
                '/users/register',
                data={
                    'email': '',
                    'password': 'password',
                    'invite': 'invite_code'
                },
                follow_redirects=True
            )
            self.assertIn(b'Please ensure you fill in all fields.',
                          response.data)
