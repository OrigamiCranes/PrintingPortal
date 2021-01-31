from app import db


class PrintOrder(db.Model):
    __tablename__ = 'print_order'
    id = db.Column(db.Integer, primary_key=True)
    dateTime = db.Column(db.DateTime, nullable=True)
    paperSize = db.Column(db.Integer, db.ForeignKey('paper_size.id'), nullable=False)
    paperType = db.Column(db.Integer, db.ForeignKey('paper_type.id'), nullable=False)
    printProduct = db.Column(db.Integer, db.ForeignKey('print_product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class PrintOrderHistory(db.Model):
    __tablename__ = 'print_order_history'
    id = db.Column(db.Integer, primary_key=True)
    dateTime = db.Column(db.DateTime, nullable=True)
    paperSize = db.Column(db.Integer, db.ForeignKey('paper_size.id'), nullable=False)
    paperType = db.Column(db.Integer, db.ForeignKey('paper_type.id'), nullable=False)
    printProduct = db.Column(db.Integer, db.ForeignKey('print_product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class PaperSize(db.Model):
    __tablename__ = 'paper_size'
    id = db.Column(db.Integer, primary_key=True)
    paperSize = db.Column(db.String(50), nullable=False)

    printOrders = db.relationship('PrintOrder', backref='paper_size')
    printOrdersHistory = db.relationship('PrintOrderHistory', backref='paper_size')


class PaperType(db.Model):
    __tablename__ = 'paper_type'
    id = db.Column(db.Integer, primary_key=True)
    paperType = db.Column(db.String(50), nullable=False, unique=True)

    printOrders = db.relationship('PrintOrder', backref='paper_type')
    printOrdersHistory = db.relationship('PrintOrderHistory', backref='paper_type')


class PrintProduct(db.Model):
    __tablename__ = 'print_product'
    id = db.Column(db.Integer, primary_key=True)
    design = db.Column(db.String(120), nullable=False, unique=True)

    printOrders = db.relationship('PrintOrder', backref='print_product')
    printOrdersHistory = db.relationship('PrintOrderHistory', backref='print_product')

from . import dataseed



