#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for links module."""


from tests.base import BaseTestCase


class UsersTestCase(BaseTestCase):

    """Links test cases."""

    def test_links_page(self):
        """Test /links route."""
        response = self.client.get('/links', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add new link:', response.data)
