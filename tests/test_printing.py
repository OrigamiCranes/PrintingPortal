from tests.test_base import TestBase
from flask import url_for
from app.blueprints.printing.forms import formPrinterQuery_factory

class TestRoutes(TestBase):
    def test_access_index(self):
        response = self.client.get(url_for('printing.index'))
        self.assertEqual(response.status_code, 200)

    def test_access_index_row(self):
        response = self.client.post(url_for('printing.index', row_id=1), follow_redirects=True)
        self.assertIn(b'Print Order', response.data)

    def test_access_add(self):
        response = self.client.post(url_for('printing.add'), follow_redirects=True)
        self.assertIn('printOrder', response.location)
        self.assertEqual(response.status_code, 304)

    def test_access_delete(self):
        response = self.client.post(url_for('printing.delete', row_id=1), follow_redirects=True)
        self.assertIn(b'Print Order', response.data)

    def test_access_edit(self):
        response = self.client.post(url_for('printing.edit', row_id=1), follow_redirects=True)
        self.assertIn('printOrder', response.location)
        self.assertEqual(response.status_code, 304)

    def test_access_clear(self):
        response = self.client.post(url_for('printing.clear'), follow_redirects=True)
        self.assertIn(b'Print Order', response.data)

    def test_access_checkout(self):
        response = self.client.post(url_for('printing.checkout'), follow_redirects=True)
        self.assertIn(b'Print Order', response.data)

    def test_access_orderHistory(self):
        response = self.client.post(url_for('printing.orderHistory'), follow_redirects=True)
        self.assertIn(b'Print Order History', response.data)

    def test_access_printInventory(self):
        response = self.client.post(url_for('printing.inventoryPrints'), follow_redirects=True)
        self.assertIn(b'Print Inventory', response.data)

    def test_access_settings(self):
        response = self.client.get(url_for('printing.settings'), follow_redirects=True)
        self.assertIn(b'Settings', response.data)

    def test_post_add(self):
        response = self.client.post(url_for('printing.add', paperSize=1, paperType=1,
                                            printProduct=1, quantity=1),
                                    follow_redirects=True)
        self.assertIn(b'Print Order', response.data)

        response = self.client.post(url_for('printing.add', paperSize=1111, paperType=1,
                                            printProduct=1, quantity=1),
                                    follow_redirects=True)
        self.assertIn('printOrder', response.location)
        self.assertEqual(response.status_code, 304)

    # def test_post_checkout(self):
    #    self.client.post(url_for('printing.add', paperSize=1, paperType=1,
    #                             printProduct=1, quantity=1),
    #                     follow_redirects=True)
    #    response = self.client.post(url_for('printing.checkout'), follow_redirects=True)
    #    self.assertIn(b'Print Order', response.data)

    def test_post_edit(self):
        self.client.post(url_for('printing.add', paperSize=1, paperType=1,
                                 printProduct=1, quantity=1),
                         follow_redirects=True)

        response = self.client.post(url_for('printing.edit', row_id=1,  paperSize=1, paperType=1,
                                            printProduct=1, quantity=1),
                                    follow_redirects=True)
        self.assertIn(b'Print Order', response.data)

        response = self.client.post(url_for('printing.edit', row_id=1, paperSize=11111, paperType=1,
                                            printProduct=1, quantity=1),
                                    follow_redirects=True)
        self.assertIn('printOrder', response.location)
        self.assertEqual(response.status_code, 304)

class TestForms(TestBase):
    def test_form_add(self):
        formAdd = formPrinterQuery_factory('Add')
        self.assertIs(formAdd.form_type, 'Add')

    def test_form_edit(self):
        response = self.client.post(url_for('printing.add', paperSize=1, paperType=1,
                                            printProduct=1, quantity=1),
                                    follow_redirects=True)
        self.assertIn(b'Print Order', response.data)

        formEdit = formPrinterQuery_factory('Edit', row_id=1)
        self.assertIs(formEdit.form_type, 'Edit')

    def test_form_filter(self):
        formFilter = formPrinterQuery_factory('Filter')
        self.assertIs(formFilter.form_type, 'Filter')
