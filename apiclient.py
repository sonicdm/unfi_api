from datetime import date, timedelta
from unfi_api import UnfiApiClient, UnfiAPI
import os
from tqdm import tqdm
from unfi_api import invoice
from unfi_api.invoice import OrderList
import logging

logging.basicConfig(filename='apiclient.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)
# set output log file

if __name__ == '__main__':
    api = UnfiAPI(os.environ['UNFI_USER'], os.environ['UNFI_PASSWORD'], False)
    client = UnfiApiClient(api)
    # result = client.search("field day")
    invoice_list: OrderList = client.get_invoice_list()
    filtered_invoice_list = invoice_list.filter_by_date(date.today()-timedelta(days=3), date.today())

    with tqdm(total=len(filtered_invoice_list)) as pbar:
        invoices = client.get_invoices(filtered_invoice_list, threaded=True, callback=lambda x: pbar.update())

            # print(invoice.get_invoice_pdf())
    print(invoices)
    input("Press Enter to continue...")
    pass
    pass