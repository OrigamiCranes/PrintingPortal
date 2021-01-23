from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms.validators import DataRequired


class PrinterFormAdd(FlaskForm):
    printProduct = wtf.SelectField()
    paperSize = wtf.SelectField()
    paperType = wtf.SelectField()
    quantity = wtf.IntegerField()
    submit = wtf.SubmitField()


class PrinterFormBasket(FlaskForm):
    clear = wtf.SubmitField()
    checkout = wtf.SubmitField()

