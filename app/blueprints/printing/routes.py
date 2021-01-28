from . import bp, forms, models
from flask import render_template, make_response, request, session
from flask_login import login_required
# from flask_user roles_required
import datetime
from app import db


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    formPAQ = forms.PrinterFormAddQuery()
    formBasket = forms.PrinterFormBasket()
    formDelete = forms.PrinterOrderDelete()

    if formPAQ.validate_on_submit():
        print(formPAQ.quantity.data)
        dateTime = datetime.datetime.now()
        order = models.PrintOrder(dateTime=dateTime)
        order.paperSize = formPAQ.paperSize.data.id
        order.paperType = formPAQ.paperType.data.id
        order.printProduct = formPAQ.printProduct.data.id
        order.quantity = formPAQ.quantity.data
        print(order)
        db.session.add(order)
        db.session.commit()

    if formDelete.validate_on_submit() and formDelete.x.data:
        request_id = int(formDelete.printOrder_id.data)
        db.session.query(models.PrintOrder).filter_by(id=request_id).delete()
        db.session.commit()

    if formBasket.validate_on_submit():
        if formBasket.clear.data is True:
            db.session.query(models.PrintOrder).delete()
            db.session.commit()

        elif formBasket.checkout.data is True:
            pass

    printOrder_columns = ['DateTime', 'Print Design', 'Size', 'Paper Type', 'Quantity']
    return render_template('printing/index.html', title='Printing', formAddQ=formPAQ, formBasket=formBasket,
                           formDelete=formDelete,
                           printOrders=db.session.query(models.PrintOrder).all(),
                           printOrders_columns=printOrder_columns)
