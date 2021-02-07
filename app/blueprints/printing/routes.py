from . import bp, forms, models
from flask import render_template, make_response, request, session, redirect, url_for
from flask_login import login_required
# from flask_user roles_required
import datetime
import wtforms as wtf
from app import db

printOrder_columns = ['DateTime', 'Print Design', 'Size', 'Paper Type', 'Quantity']
printInventory_columns = ['Print Design', 'Size', 'Paper Type', 'Quantity']


@bp.route('/printOrder/<int:row_id>', methods=['GET', 'POST'])
@bp.route('/printOrder', methods=['GET', 'POST'])
@login_required
def index(row_id=None):

    # 1. Declare Forms
    formAdd = forms.formPrinterQuery_factory('Add')
    formBasket = forms.PrinterFormBasket()
    formSettings = forms.PrinterOrderSettings()
    formEdit = None

    if row_id is not None:
        formEdit = forms.formPrinterQuery_factory('Edit', row_id=row_id)

        if formEdit is False:
            return redirect(url_for('.index'))

        if formEdit.validate_on_submit() and formEdit.submit.data:
            return redirect(url_for('.edit', row_id=row_id,
                                    paperSize=formEdit.paperSize.data.id,
                                    paperType=formEdit.paperType.data.id,
                                    printProduct=formEdit.printProduct.data.id,
                                    quantity=formEdit.quantity.data), code=307)

        elif formEdit.cancel.data:
            return redirect(url_for('.index'))

    # 2. POST Validate Forms
    if formAdd.validate_on_submit():
        return redirect(url_for('.add', row_id=row_id,
                                paperSize=formAdd.paperSize.data.id,
                                paperType=formAdd.paperType.data.id,
                                printProduct=formAdd.printProduct.data.id,
                                quantity=formAdd.quantity.data), code=307)

    if formSettings.validate_on_submit():
        if formSettings.delete.data:
            request_id = int(formSettings.printOrder_id.data)
            return redirect(url_for('.delete', row_id=request_id))

        if formSettings.edit.data:
            request_id = int(formSettings.printOrder_id.data)
            formSettings.edit.data = False
            return redirect(url_for('.index', row_id=request_id))

    if formBasket.validate_on_submit():
        if formBasket.clear.data is True:
            return redirect(url_for('.clear'), code=307)

        elif formBasket.checkout.data is True:
            return redirect(url_for('.checkout'), code=307)

    return render_template('printing/index.html', title='Printing', formAdd=formAdd, formBasket=formBasket,
                           formRowSettings=formSettings, formRowEdit=formEdit, edit_id=row_id,
                           table_data=db.session.query(models.PrintOrder).all(),
                           table_headers=printOrder_columns, table_settings=True)


@bp.route('/printOrder/add', methods=['POST'])
@login_required
def add():
    # 1. Get Input Variables
    inputs = [request.args.get('paperSize', None), request.args.get('paperType', None),
              request.args.get('printProduct', None), request.args.get('quantity', None)]

    # 2. Error checking http based variables for safety
    columns = ['models.PaperSize', 'models.PaperType', 'models.PrintProduct','quantity']
    for n, item in enumerate(inputs):
        print(n)
        if item is None or isinstance(item, int):
            return redirect(url_for('.index'), code=304)
        if n is not 3:
            if db.session.query(eval(columns[n])).filter_by(id=item).scalar() is None:
                print('error' + str(n))
                return redirect(url_for('.index'), code=304)


    dateTime = datetime.datetime.now()
    dateTime = dateTime.replace(microsecond=0)

    order = models.PrintOrder(
        dateTime=dateTime,
        paperSize=inputs[0],
        paperType=inputs[1],
        printProduct=inputs[2],
        quantity=inputs[3])

    db.session.add(order)
    db.session.commit()
    return redirect(url_for('.index'))


@bp.route('/printOrder/<int:row_id>/delete', methods=['POST'])
@login_required
def delete(row_id):
    db.session.query(models.PrintOrder).filter_by(id=row_id).delete()
    db.session.commit()
    return redirect(url_for('.index'))


@bp.route('/printOrder/<int:row_id>/edit', methods=['POST'])
@login_required
def edit(row_id):
    # 1. Get Input Variables
    inputs = [request.args.get('paperSize', None), request.args.get('paperType', None),
              request.args.get('printProduct', None), request.args.get('quantity', None)]

    # 2. Error checking http based variables for safety
    columns = ['models.PaperSize', 'models.PaperType', 'models.PrintProduct', 'quantity']
    for n, item in enumerate(inputs):
        print(n)
        if item is None or isinstance(item, int):
            return redirect(url_for('.index'), code=304)
        if n is not 3:
            if db.session.query(eval(columns[n])).filter_by(id=item).scalar() is None:
                print('error' + str(n))
                return redirect(url_for('.index'), code=304)

    row_update = db.session.query(models.PrintOrder).filter_by(id=row_id).one()
    row_update.paperSize = inputs[0]
    row_update.paperType = inputs[1]
    row_update.printProduct = inputs[2]
    row_update.quantity = inputs[3]

    db.session.commit()
    return redirect(url_for('.index'))


@bp.route('/printOrder/clear', methods=['POST'])
@login_required
def clear():
    db.session.query(models.PrintOrder).delete()
    db.session.commit()
    return redirect(url_for('.index'))


@bp.route('/printOrder/checkout', methods=['POST'])
@login_required
def checkout():
    if bool(db.session.query(models.PrintOrder).first()) is False:
        return redirect(url_for('.index'))

    # 1. Transfer from table printOrder to table printOrderHistory
    printOrders = db.session.query(models.PrintOrder).all()

    for order in printOrders:
        printHistory_row = models.PrintOrderHistory(
            dateTime=order.dateTime,
            paperSize=order.paperSize,
            paperType=order.paperType,
            printProduct=order.printProduct,
            quantity=order.quantity)
        db.session.add(printHistory_row)
    db.session.query(models.PrintOrder).delete()
    db.session.commit()

    # 2. Make Inventory Query
    inventory_new = db.engine.execute('SELECT printProduct, paperSize, paperType, COUNT(*) AS quantity FROM print_order_history GROUP BY paperSize, paperType, printProduct')

    # 3. Delete Print Inventory and Pass inventory_new to a new table
    db.session.query(models.PrintInventory).delete()
    db.session.execute("ALTER TABLE print_inventory AUTO_INCREMENT = 1")
    db.session.commit()

    for item in inventory_new:
        inventory_row = models.PrintInventory(
            printProduct=db.session.query(models.PrintProduct).filter_by(id=item.printProduct).one().id,
            paperSize=db.session.query(models.PaperSize).filter_by(id=item.paperSize).one().id,
            paperType=db.session.query(models.PaperType).filter_by(id=item.paperType).one().id,
            quantity=item.quantity)
        db.session.add(inventory_row)

    db.session.commit()

    return redirect(url_for('.index'))


@bp.route('/printOrder/history', methods=['GET', 'POST'])
@login_required
def orderHistory():

    formFilter = forms.formPrinterQuery_factory('Filter')
    table_settings = False

    if formFilter.submit.data:
        filter_data = []
        for field in formFilter:
            if field.data is None:
                filter_data.append('%')
            elif field.type is 'IntegerField':
                filter_data.append(field.data)
            elif field.type is 'QuerySelectField':
                filter_data.append(field.data.id)

        printOrders = db.session.query(models.PrintOrderHistory).filter(
            models.PrintOrderHistory.printProduct.like(filter_data[0]),
            models.PrintOrderHistory.paperSize.like(filter_data[1]),
            models.PrintOrderHistory.paperType.like(filter_data[2]),
            models.PrintOrderHistory.quantity.like(filter_data[3])
        )
    else:
        printOrders = db.session.query(models.PrintOrderHistory).all()

    return render_template('printing/printOrder_history.html', title='Print Order History',
                           formAdd=formFilter,
                           table_data=printOrders, table_headers=printOrder_columns,
                           table_settings=table_settings)


@bp.route('/paper/settings',  methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('printing/settings.html')


@bp.route('/inventory/prints', methods=['GET', 'POST'])
def inventoryPrints():
    formFilter = forms.formPrinterQuery_factory('Filter')
    table_settings = False

    if formFilter.submit.data:
        filter_data = []
        for field in formFilter:
            if field.data is None:
                filter_data.append('%')
            elif field.type is 'IntegerField':
                filter_data.append(field.data)
            elif field.type is 'QuerySelectField':
                filter_data.append(field.data.id)

        printInventory = db.session.query(models.PrintInventory).filter(
            models.PrintInventory.printProduct.like(filter_data[0]),
            models.PrintInventory.paperSize.like(filter_data[1]),
            models.PrintInventory.paperType.like(filter_data[2]),
            models.PrintInventory.quantity.like(filter_data[3])
        )
    else:
        printInventory = db.session.query(models.PrintInventory).all()

    return render_template('printing/printInventory.html', title='Print Inventory',
                           formAdd=formFilter,
                           table_data=printInventory, table_headers=printInventory_columns,
                           table_settings=table_settings)