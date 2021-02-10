import unittest
from unittest import TestCase
import codecs
from unfi_api import UnfiAPI
from unfi_api.api.order_management import parse_invoice_html_to_json


class TestInvoices(unittest.TestCase):

    def test_get_invoice_list(self):
        pass


class TestOrderHistory(TestCase):
    def test_get_invoice(self):
        with codecs.open(r"../../assets/ordermanagement/orderhistory/GetCreditInvoiceDetailForWest.html") as page:
            content = str(page.read())
        parsed = parse_invoice_html_to_json(content)
        pass
