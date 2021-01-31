from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from . import models
from wtforms.validators import DataRequired


# Legacy Class - not used
class PrinterFormAdd(FlaskForm):
    printProduct = wtf.SelectField()
    paperSize = wtf.SelectField()
    paperType = wtf.SelectField()
    quantity = wtf.IntegerField()
    submit = wtf.SubmitField()


class PrinterFormAddQuery(FlaskForm):
    printProduct = QuerySelectField(
        'Print Product',
        query_factory=lambda: models.PrintProduct.query,
        get_label='design',
        allow_blank=False
    )

    paperSize = QuerySelectField(
        'Paper Size',
        query_factory=lambda: models.PaperSize.query,
        get_label='paperSize',
        allow_blank=False
    )

    paperType = QuerySelectField(
        'Paper Type',
        query_factory=lambda: models.PaperType.query,
        get_label='paperType',
        allow_blank=False
    )

    quantity = wtf.IntegerField(
        default=1
    )
    submit = wtf.SubmitField()


class PrinterFormBasket(FlaskForm):
    clear = wtf.SubmitField()
    checkout = wtf.SubmitField()


class PrinterOrderDelete(FlaskForm):
    printOrder_id = wtf.HiddenField('printOrder_id')
    x = wtf.SubmitField()


class PrinterFormFilter(FlaskForm):
    printProduct = QuerySelectField(
        'Print Product',
        query_factory=lambda: models.PrintProduct.query,
        get_label='design',
        allow_blank=True
    )

    paperSize = QuerySelectField(
        'Paper Size',
        query_factory=lambda: models.PaperSize.query,
        get_label='paperSize',
        allow_blank=True
    )

    paperType = QuerySelectField(
        'Paper Type',
        query_factory=lambda: models.PaperType.query,
        get_label='paperType',
        allow_blank=True
    )

    quantity = wtf.IntegerField()
    submit = wtf.SubmitField()

