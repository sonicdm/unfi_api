from unfi_api import UnfiApiClient, UnfiAPI
import os

if __name__ == '__main__':
    api = UnfiAPI(os.environ['UNFI_USER'], os.environ['UNFI_PASS'], False)
    client = UnfiApiClient(api)
    # result = client.search("field day")
    invoice_list = client.get_invoice_list()
    pass