# import datetime
# import unittest

# # import catalogboss.catalog.products
# # from unfi_api import unfi_invoice
# # from unfi_api.unfi_invoice import parse_invoices
# from unfi_api.unfi_web_queries import pull_invoices, get_invoice_list, create_invoice_workbook
# from unfi_api import UnfiAPI
# # from catalogboss.catalogio import read_workbook

# TEST_INVOICE = r"C:\Users\Administrator\Desktop\UNFI SCRIPTS\CatalogBoss\Test_Invoices\066463179-003.xlsx"
# TEST_BATCH = r"C:\Users\Administrator\Desktop\UNFI SCRIPTS\CatalogBoss\Test_Invoices\066463179-003-batch.xlsx"
# TEST_INVOICE_BOOK = r"C:\Users\Administrator\Desktop\UNFI SCRIPTS\CatalogBoss\Test_Invoices\invoice_book.xlsx"
# TEST_INVENTORY = r"F:\Grocery\Receiving\Temp\test inventory.csv"
# TEST_OUTPUT_PATH = r"C:\Users\Administrator\Desktop\UNFI SCRIPTS\CatalogBoss\Test_Invoices\output.xlsx"


# class InvoiceTests(unittest.TestCase):
#     def test_make_filename(self):
#         date = '01/03/2019'
#         outputfolder = r"C:\test"
#         invoice_expected = "2019-01-03 - Grocery - 0129302-003"
#         realdate = datetime.datetime.strptime(date, "%m/%d/%Y")
#         self.assertEqual(unfi_invoice.make_filename(realdate, '0129302-003', "Grocery"), invoice_expected)
#         no_invoice = "2019-01-03 - Grocery"

#     def test_create_invoice(self):
#         invwb = read_workbook(TEST_INVOICE)
#         invoice = unfi_invoice.Invoice(invwb['workbook'][0], 123, "grocery")

#     def test_create_product(self):
#         product = catalogboss.catalog.products.Product(7341002619)

#     def test_inventory(self):
#         invwb = read_workbook(TEST_INVENTORY)
#         inventory = unfi_invoice.Inventory(invwb, 750)

#     def test_parse_invoices(self):
#         invoicedict = read_workbook(r'F:\Recieving\UNFI Check In\09-06-2019\invoices.xlsx')
#         parse_invoices(invoicedict)

#     def test_make_invoice_workbook(self):
#         inventorywb = read_workbook(TEST_INVENTORY)
#         inventory = unfi_invoice.Inventory(inventorywb, 700)
#         invoicebook = read_workbook(TEST_INVOICE_BOOK)
#         invoices = unfi_invoice.parse_invoices(invoicebook, inventory)

#     def test_inventory_report(self):
#         report = unfi_invoice.InventoryReport(TEST_INVENTORY, TEST_INVOICE_BOOK)

#     def test_write_report(self):
#         report = unfi_invoice.InventoryReport(TEST_INVENTORY, TEST_INVOICE_BOOK)
#         report.write(TEST_OUTPUT_PATH)

#     def test_create_invoice_workbook(self):
#         from datetime import datetime, date
#         print("Logging In...")
#         api = UnfiAPI("grocery@capellamarket.com", "Organic1")
#         token = api.auth_token
#         invdate = date(2019, 9, 6)
#         invoices = pull_invoices(token, invdate)
#         invoice_wb = create_invoice_workbook(invoices)
#         pass

#     def test_get_invoice_list(self):
#         print("Logging In...")
#         api = UnfiAPI("grocery@capellamarket.com", "Organic1")
#         token = api.auth_token

#         invoice_list = get_invoice_list(token, datetime.datetime.today())
#         pass


# if __name__ == "__main__":
#     unittest.main()
