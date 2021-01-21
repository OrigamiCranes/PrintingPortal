from app import db


class PrintOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dateTime = db.Column(db.DateTime)
    paperSize_id = db.Column(db.Integer)
    paperType_id = db.Column(db.Integer)
    printProduct_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)


class PaperSize(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paperSize = db.Column(db.String(50), nullable=False)


class PaperType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paperType = db.Column(db.String(50), nullable=False)


class PrintProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    design = db.Column(db.String(120), nullable=False)