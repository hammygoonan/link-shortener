#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""create_db.py: Create database and a range of dummy data for testing."""


from shortener import db
from shortener.models import User, Invitation


def create_db():
    """Create database for tests."""
    db.create_all()
    db.session.add(User('hammy@spiresoftware.com.au', 'password'))
    db.session.add(User('test@spiresoftware.com.au', 'password'))
    db.session.add(Invitation('hammy2@spiresoftware.com.au', 'invite_code'))
    db.session.commit()
