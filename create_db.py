#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""create_db.py: Create database and a range of dummy data for testing."""


from shortener import db
from datetime import datetime, timedelta
from shortener.models import User, Invitation, ResetPassword


def create_db():
    """Create database for tests."""
    db.create_all()
    user = User('hammy@spiresoftware.com.au', 'password')
    user2 = User('test@spiresoftware.com.au', 'password')
    db.session.add(user)
    db.session.add(user2)
    db.session.add(Invitation('hammy2@spiresoftware.com.au', 'invite_code'))
    db.session.add(ResetPassword(user, 'resetcode',
                                 datetime.utcnow() + timedelta(hours=24)))
    db.session.add(ResetPassword(user2, 'resetcode2',
                                 datetime.utcnow() - timedelta(hours=24)))
    db.session.commit()
