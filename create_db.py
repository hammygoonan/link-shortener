#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""create_db.py: Create database and a range of dummy data for testing."""


from shortener import db
from datetime import datetime, timedelta
from shortener.models import User, Invitation, ResetPassword, Link


def create_db():
    """Create database for tests."""
    db.create_all()
    user = User('test_1@example.com', 'password')
    user2 = User('test_3@example.com', 'other_password')
    db.session.add(user)
    db.session.add(user2)
    db.session.add(Invitation('test_4@example.com', 'invite_code'))
    db.session.add(ResetPassword(user, 'resetcode',
                                 datetime.utcnow() + timedelta(hours=24)))
    db.session.add(ResetPassword(user2, 'resetcode2',
                                 datetime.utcnow() - timedelta(hours=24)))

    # add some links
    links = [('http://example.com', 'slug11'),
             ('http://google.com', 'slug22'),
             ('https://news.ycombinator.com/', 'slug33'),
             ('http://flask.pocoo.org', 'slug44'),
             ('https://www.python.org/', 'slug55')]
    for link in links:
        db.session.add(Link(link[0], link[1], user))

    links = [('http://test.com', 'slug66'),
             ('http://yahoo.com', 'slug77')]
    for link in links:
        db.session.add(Link(link[0], link[1], user2))

    db.session.commit()
