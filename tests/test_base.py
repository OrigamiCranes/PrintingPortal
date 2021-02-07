import unittest
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import upgrade, downgrade

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
        path = os.path.dirname(os.path.dirname(__file__)) + "\migrations"
        upgrade(directory=os.path.abspath(path))
        db.create_all()

        from app.blueprints.printing import dataseed as printing_dataseed
        printing_dataseed.data()

        from app.blueprints.auth import dataseed as auth_dataseed
        auth_dataseed.data()





        # data

    def tearDown(self):
        path = os.path.dirname(os.path.dirname(__file__)) + "\migrations"
        db.drop_all()
        db.session.remove()

        os.remove(os.path.join(basedir, 'test.db'))


    def add_data(self):
        paperSizes = [
            models.PaperSize(paperSize='A3'),
            models.PaperSize(paperSize='A4'),
            models.PaperSize(paperSize='A5')
        ]
        db.session.bulk_save_objects(paperSizes)
        db.session.commit()
        #
        PaperTypes = [
            models.PaperType(paperType='Glossy'),
            models.PaperType(paperType='WaterColour'),
            models.PaperType(paperType='Matte')
        ]
        #
        db.session.bulk_save_objects(PaperTypes)
        db.session.commit()

        PrintProducts = [
            models.PrintProduct(design='Eevee'),
            models.PrintProduct(design='Finn'),
            models.PrintProduct(design='Taro'),
            models.PrintProduct(design='Tiger'),
            models.PrintProduct(design='RitualCat')
        ]
        db.session.bulk_save_objects(PrintProducts)
        db.session.commit()


