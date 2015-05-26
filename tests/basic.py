#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.base import BaseTestCase

class BasicTestCase(BaseTestCase):
    """Basic test cases."""

    def test_hello_world(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home Page', response.data)
