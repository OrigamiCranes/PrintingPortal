import unittest
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy

from app import *
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class TestBase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'test.db')
        app.config['TESTING'] = True
        app.config['LOGIN_DISABLED'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        return app

    def setUp(self):
        db.create_all()

        from app.blueprints.auth import dataseed
        from app.blueprints.printing import dataseed

        # data

    def tearDown(self):
        db.drop_all()
        #os.remove(os.path.join(basedir, 'test.db'))




