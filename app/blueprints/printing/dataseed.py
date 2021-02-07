from app import db
from . import models


# CREATE BASIC DATA
def data():
    if db.engine.dialect.has_table(db.engine, 'paper_size'):
        if db.session.query(models.PaperSize).count() == 0:
            paperSizes = [
                models.PaperSize(paperSize='A3'),
                models.PaperSize(paperSize='A4'),
                models.PaperSize(paperSize='A5')
            ]
            db.session.bulk_save_objects(paperSizes)
            db.session.commit()
            print("PaperSize Entries: " + str(db.session.query(models.PaperSize).count()))

    if db.engine.dialect.has_table(db.engine, 'paper_type'):
        if db.session.query(models.PaperType).count() == 0:
            PaperTypes = [
                models.PaperType(paperType='Glossy'),
                models.PaperType(paperType='WaterColour'),
                models.PaperType(paperType='Matte')
            ]
            db.session.bulk_save_objects(PaperTypes)
            db.session.commit()
            print("PaperType Entries: " + str(db.session.query(models.PaperType).count()))

    if db.engine.dialect.has_table(db.engine, 'print_product'):
        if db.session.query(models.PrintProduct).count() == 0:
            PrintProducts = [
                models.PrintProduct(design='Eevee'),
                models.PrintProduct(design='Finn'),
                models.PrintProduct(design='Taro'),
                models.PrintProduct(design='Tiger'),
                models.PrintProduct(design='RitualCat')
            ]
            db.session.bulk_save_objects(PrintProducts)
            db.session.commit()
            print("Print Product Entries: " + str(db.session.query(models.PrintProduct).count()))


data()