from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from . import models
from app import db
from wtforms.validators import DataRequired


def formPrinterQuery_factory(form_type, row_id=None):
    allow_blank = False
    default = [None, None, None, None]
    if form_type is 'Add':
        default[3] = 1

    elif form_type is 'Filter':
        allow_blank = True

    elif form_type is 'Edit':
        row_update = db.session.query(models.PrintOrder).filter_by(id=row_id).first()
        if row_update is None:
            return False

        default = [models.PrintProduct.query.filter_by(id=row_update.printProduct).one(),
                   models.PaperSize.query.filter_by(id=row_update.paperSize).one(),
                   models.PaperType.query.filter_by(id=row_update.paperType).one(),
                   int(row_update.quantity)]

    else:
        raise Exception('form_type: ' + str(form_type) + ' not found')

    class FormPrinterQuery(FlaskForm):
        printProduct = QuerySelectField(
            'Print Product',
            query_factory=lambda: models.PrintProduct.query,
            get_label='design',
            allow_blank=allow_blank,
            default=default[0])

        paperSize = QuerySelectField(
            'Paper Size',
            query_factory=lambda: models.PaperSize.query,
            get_label='paperSize',
            allow_blank=allow_blank,
            default=default[1])

        paperType = QuerySelectField(
            'Paper Type',
            query_factory=lambda: models.PaperType.query,
            get_label='paperType',
            allow_blank=allow_blank,
            default=default[2])

        quantity = wtf.IntegerField(
            default=default[3])

        submit = wtf.SubmitField()

        if form_type is 'Edit':
            cancel = wtf.SubmitField()

    form = FormPrinterQuery()
    form.form_type = form_type
    return form


class PrinterFormBasket(FlaskForm):
    clear = wtf.SubmitField()
    checkout = wtf.SubmitField()


class PrinterOrderSettings(FlaskForm):
    printOrder_id = wtf.HiddenField('printOrder_id')
    delete = wtf.SubmitField()
    edit = wtf.SubmitField()


