#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for links module."""


from tests.base import BaseTestCase


class UsersTestCase(BaseTestCase):

    """Links test cases."""

    def test_links_page_not_logged_in(self):
        """Test /links route when NOT logged in."""
        response = self.client.get(
            '/links', content_type='html/text',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_links_page_logged_in(self):
        """Test /links route when loggen in."""
        response = self.client.get(
            '/users/login', content_type='html/text',
            follow_redirects=True,
            data=dict(
                email='hammy@spiresoftware.com.au',
                password='password'
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Link', response.data)
