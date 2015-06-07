#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for links module."""


from flask.ext.login import current_user
from tests.base import BaseTestCase
from shortener.models import Link
from mock import patch
from mock import MagicMock
import requests


class LinkTestCase(BaseTestCase):

    """Link test cases."""

    def setUp(self):
        """Setup User tests."""
        self.email = 'test_1@example.com'
        self.password = 'password'
        super().setUp()

    def test_links_page_not_logged_in(self):
        """Test /links route when NOT logged in."""
        response = self.client.get(
            '/list', content_type='html/text',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login to view that page.', response.data)

    def test_number_of_links_on_page(self):
        """Test that there is the corect number of links on the page."""
        with self.client:
            self.client.post(
                '/users/login',
                data={'email': self.email, 'password': self.password},
                follow_redirects=True
            )
            response = self.client.get('/list')
            self.assertIn(b'http://example.com', response.data)
            self.assertIn(b'http://google.com', response.data)
            self.assertIn(b'https://news.ycombinator.com', response.data)
            self.assertIn(b'http://flask.pocoo.org', response.data)
            self.assertIn(b'https://www.python.org', response.data)

            # make sure the links of other users aren't there
            self.assertNotIn(b'http://test.com', response.data)
            self.assertNotIn(b'http://yahoo.com', response.data)

    @patch.object(requests, 'get')
    def test_add_links(self, get_mock):
        """Test the various combinations of adding links."""
        get_mock.return_value = mock_get_response = MagicMock()
        mock_get_response.content = "<title>this is some content</title>"
        mock_get_response.status_code = 200
        with self.client:
            self.client.post(
                '/users/login',
                data={'email': self.email, 'password': self.password},
                follow_redirects=True
            )
            # check link is added
            response = self.client.post(
                '/add',
                data={'url': 'http://newlink.com'}
            )
            self.assertIn(b'Your link was added - http://newlink.com',
                          response.data)
            self.assertTrue(
                Link.query.filter_by(
                    user_id=current_user.id, url='http://newlink.com'
                ).first()
            )
            # check link is valid
            response = self.client.post(
                '/add',
                data={'url': 'http:/newlink.com'}
            )
            self.assertIn(b'That link isn&#39;t formatted correctly.',
                          response.data)
            self.assertFalse(
                Link.query.filter_by(
                    user_id=current_user.id, url='http:/newlink.com'
                ).first()
            )
            # check link isn't added twice
            response = self.client.post(
                '/add',
                data={'url': 'http://newlink.com'}
            )
            self.assertIn(b'http://newlink.com - has been added previously.',
                          response.data)
            new_link = Link.query.filter_by(user_id=current_user.id,
                                            url='http://newlink.com').all()
            self.assertTrue(1 == len(new_link))
            self.assertTrue('this is some content' == new_link[0].title)

    def test_link_redirect(self):
        """Test redirects work."""
        with self.client:
            response = self.client.get(
                '/slug22',
                follow_redirects=False
            )
            self.assertEqual(response.location, 'http://google.com')

        with self.client:
            response = self.client.get(
                '/test',
                follow_redirects=True
            )
            self.assert404(response)
