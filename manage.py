#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from flask.ext.script import Manager
from shortener import app, db

manager = Manager(app)


@manager.command
def test():
	"""Runs unit tests."""

	tests = unittest.TestLoader().discover('', pattern='*.py')
	unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
	manager.run()
