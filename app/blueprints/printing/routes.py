from . import bp, forms, models
from flask import render_template, make_response, request, session, redirect, url_for
from flask_login import login_required
# from flask_user roles_required
import datetime
import wtforms as wtf
from app import db

printOrder_columns = ['DateTime', 'Print Design', 'Size', 'Paper Type', 'Quantity']

@bp.route('/printOrder', methods=['GET', 'POST'])
@login_required
def index():

    # 1. Declare Forms
    formPAQ = forms.PrinterFormAddQuery()
    formBasket = forms.PrinterFormBasket()
    formDelete = forms.PrinterOrderDelete()

    # 2. POST Validate Forms
    if formPAQ.validate_on_submit():
        dateTime = datetime.datetime.now()
        order = models.PrintOrder(
            dateTime=dateTime,
            paperSize=formPAQ.paperSize.data.id,
            paperType=formPAQ.paperType.data.id,
            printProduct=formPAQ.printProduct.data.id,
            quantity=formPAQ.quantity.data)
        db.session.add(order)
        db.session.commit()

    if formDelete.validate_on_submit():
        if formDelete.delete.data:
            request_id = int(formDelete.printOrder_id.data)
            db.session.query(models.PrintOrder).filter_by(id=request_id).delete()
            db.session.commit()

        if formDelete.edit.data:
            request_id = int(formDelete.printOrder_id.data)
            return redirect(url_for('.edit', row_id=request_id))


    if formBasket.validate_on_submit():
        if formBasket.clear.data is True:
            db.session.query(models.PrintOrder).delete()
            db.session.commit()

        elif formBasket.checkout.data is True:
            printOrders = db.session.query(models.PrintOrder).all()

            for order in printOrders:
                printHistory_row = models.PrintOrderHistory(
                    dateTime=order.dateTime,
                    paperSize=order.paperSize,
                    paperType=order.paperType,
                    printProduct=order.printProduct,
                    quantity=order.quantity
                )
                db.session.add(printHistory_row)

            db.session.query(models.PrintOrder).delete()
            db.session.commit()

    return render_template('printing/index.html', title='Printing', formAddQ=formPAQ, formBasket=formBasket,
                           formDelete=formDelete,
                           printOrders=db.session.query(models.PrintOrder).all(),
                           printOrders_columns=printOrder_columns)


@bp.route('/printOrder/edit/<int:row_id>', methods=['GET', 'POST'])
@login_required
def edit(row_id):

    updateRow = db.session.query(models.PrintOrder).filter_by(id=row_id).one()

    formPEQ = forms.printerFormEditQuery_factory(updateRow)()
    formDelete = forms.PrinterOrderDelete()

    if formPEQ.validate_on_submit() and formPEQ.submit.data:
        updateRow.paperSize = formPEQ.paperSize.data.id
        updateRow.paperType = formPEQ.paperType.data.id
        updateRow.printProduct = formPEQ.printProduct.data.id
        updateRow.quantity = formPEQ.quantity.data
        db.session.commit()

        return redirect(url_for('.index'))

    elif formPEQ.cancel.data:
        return redirect(url_for('.index'))

    return render_template('printing/edit.html', title='Print Order Edit', formPEQ=formPEQ, formDelete=formDelete,
                           printOrders=db.session.query(models.PrintOrder).all(),
                           printOrders_columns=printOrder_columns,
                           edit_row=row_id)



@bp.route('/paper/settings')
@login_required
def settings():
    return render_template('printing/settings.html')


@bp.route('/printOrder/history', methods=['GET', 'POST'])
@login_required
def orderHistory():

    formFilter = forms.PrinterFormFilter()
    printOrders = db.session.query(models.PrintOrderHistory).all()

    if formFilter.submit.data:
        filter_data = []
        for field in formFilter:
            print(field.type)
            if field.data is None:
                filter_data.append('%')
            elif field.type is 'IntegerField':
                filter_data.append(field.data)
            elif field.type is 'QuerySelectField':
                filter_data.append(field.data.id)

        print(filter_data)
        printOrders = db.session.query(models.PrintOrderHistory).filter(
            models.PrintOrderHistory.printProduct.like(filter_data[0]),
            models.PrintOrderHistory.paperSize.like(filter_data[1]),
            models.PrintOrderHistory.paperType.like(filter_data[2]),
            models.PrintOrderHistory.quantity.like(filter_data[3])
        )

    return render_template('printing/filter.html', title='Print Order History',
                           printOrders=printOrders,
                           printOrders_columns=printOrder_columns,
                           formFilter=formFilter)


@bp.route('/inventory/prints')
def inventoryPrints():
    pass