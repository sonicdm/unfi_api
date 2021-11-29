from pathlib import Path

config = {
    # "username": "", # username for the api will use UNFI_USERNAME env variable if left unset
    # "password": "", # password for the api will use UNFI_PASSWORD env variable if left unset
    "query_output_path": "F:\\pos\\unfi\\query_new.xlsx", # Path to where the product search spreadsheet will be saved
    "image_output_path": "F:\\signs\\product_images", # Path to the folder where the images will be saved
    "abbreviations_path": r"F:\POS\script_assets\abbreviations.csv", # Path to abbreviations file
    "max_threads": 10, # max number of threads to use
    "log_level": "INFO", # DEBUG, INFO, WARNING, ERROR, CRITICAL
    "log_path": "logs\\unfi_api.log", # Path to where the log file will be saved
    "url_length_limit": 2000, # max length of url to send to the api
}




PRODUCT_QUERY_OUTPUT_PATH = "F:\\pos\\unfi\\query_new.xlsx"
IMAGE_OUTPUT_PATH = r"F:\Signs\product_images"
beautiful_soup_parser = "html.parser"

xdock_cust_num = "001016"
xdock_warehouse = 2
ridgefield_cust_num = "001014"
ridgefield_warehouse = 6
user_id = "34653"
api_thread_limit = 8
IMAGE_OUTPUT_PATH = r"F:\Signs\product_images"
unfi_invoice_list_xhr = 'https://ordermanagement.unfi.com/api/OrderHistory/GetGridItem?' \
                        'custNum={custnum}++++&' \
                        'UserId={userid}&' \
                        'region=West&' \
                        'TransactionType=1&' \
                        'OrderNo=&' \
                        'PONO=&' \
                        'ReqBy=&' \
                        'InvoiceNo=&' \
                        'pageSize=1000&' \
                        'pageNumber=1&' \
                        'sortExpression=&sortDirection='

invoice_xhr = "https://ordermanagement.unfi.com/api/OrderHistory/" \
              "GetCreditInvoiceDetailForWest?" \
              "invoiceNumber={invoicenum}&" \
              "customerNumber={custnum}&" \
              "command="

set_default_account_xhr = r"https://adminbackend.unfi.com/api/User/InsertSelectedAccountAsDefault"
search_url = 'https://ordermanagement.unfi.com/api/Brands/GetProductsByFullText?' \
             'fullTextQuery={query}' \
             '&organicCodes=' \
             '&attributeIds=' \
             '&salesFilters=' \
             '&brandIds=' \
             '&categoryIds=' \
             '&region=West' \
             '&warehouse={warehouse}' \
             '&accountNumber={custnum}++++' \
             '&userId={userid}' \
             '&isAdminOrAccountManager=true' \
             '&pageSize=5000' \
             '&pageNumber=1'
product_detail_url = "https://ordermanagement.unfi.com/api/ProductDetail/GetProductDetailByProductIntId" \
                     "?productintId={product_id}" \
                     "&region=West" \
                     "&accountNumber={custnum}" \
                     "&warehouse=6" \
                     "&userId={userid}"
product_data_url = "https://products.unfi.com/api/Products/GetWestProductData" \
                   "?customerNumber={custnum}" \
                   "&productCode={product_code}"
product_attribute_url = "https://products.unfi.com/api/Products/{product_id}/attributes"

promo_url = "https://ordermanagement.unfi.com/api/Brands/GetProductDetailsFromService" \
            "?custNum={custnum}" \
            "&prodCode={product_code}"


