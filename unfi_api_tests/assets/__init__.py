### Asset File Information ###
import json
from pathlib import Path

# base directory paths
thisfiledir = Path(__file__).parent
assets_path = Path(thisfiledir)
# asset subdirectories
products_dir = Path(assets_path, 'products')
ordermanagement_path = Path(assets_path, 'ordermanagement')

# ordermanagement sub directories
ordermanagement_brands_dir = Path(ordermanagement_path, 'brands')
ordermanagement_ProductDetail_dir = Path(
    ordermanagement_path, 'ProductDetail')
ordermanagement_orderhistory_dir = Path(
    ordermanagement_path, 'orderhistory')

# ordermanagement brands files
ordermanagement_brands_GetProductDetailsFromService_xml_file = Path(
    ordermanagement_brands_dir, 'GetProductDetailsFromService.xml')
ordermanagement_brands_path_GetProductsByFullText_json_file = Path(
    ordermanagement_brands_dir, 'GetProductsByFullText.json')

# ordermanagement ProductDetail files
ordermanagement_ProductDetail_GetProductDetailByProductIntId_file = Path(
    ordermanagement_ProductDetail_dir, 'GetProductDetailByProductIntId.json'
    )

# ordermanagement invoice Files:
ordermanagement_orderhistory_GetCreditInvoiceDetailForWest_file = Path(
    ordermanagement_orderhistory_dir, 'GetCreditInvoiceDetailForWest.html')

# products subdirectories
products_products_dir = Path(products_dir, 'products')

# products files
products_GetWestProductData_json_file = Path(
    products_products_dir, 'GetWestProductData.json')
int_id_json_file = Path(products_products_dir, "int_id.json")

# int_id directory
int_id_dir = Path(products_products_dir, 'int_id')

# int_id directory json files
nutrition_json_file = Path(int_id_dir, 'nutrition.json')
attributes_json_file = Path(int_id_dir, 'attributes.json')
marketing_json_file = Path(int_id_dir, 'marketing.json')
ingredients_json_file = Path(int_id_dir, 'ingredients.json')

class ProductsFiles:
    get_west_product_data_json_file: Path = products_GetWestProductData_json_file
    int_id_json_file: Path = int_id_json_file
    nutrition_json_file: Path = nutrition_json_file
    attributes_json_file: Path = attributes_json_file
    marketing_json_file: Path = marketing_json_file
    ingredients_json_file: Path = ingredients_json_file

    def __init__(self):
        # open instance variable json files and store to instance variables
        with open(self.get_west_product_data_json_file, 'r') as f:
            self.get_west_product_data_json = json.load(f)
        with open(self.int_id_json_file, 'r') as f:
            self.int_id_json = json.load(f)
        with open(self.nutrition_json_file, 'r') as f:
            self.nutrition_json = json.load(f)
        with open(self.attributes_json_file, 'r') as f:
            self.attributes_json = json.load(f)
        with open(self.marketing_json_file, 'r') as f:
            self.marketing_json = json.load(f)
        with open(self.ingredients_json_file, 'r') as f:
            self.ingredients_json = json.load(f)


class OrderManagementFiles:
    brands_GetProductDetailsFromService_xml_file: Path = ordermanagement_brands_GetProductDetailsFromService_xml_file
    brands_path_GetProductsByFullText_json_file: Path = ordermanagement_brands_path_GetProductsByFullText_json_file
    ProductDetail_GetProductDetailByProductIntId_file: Path = ordermanagement_ProductDetail_GetProductDetailByProductIntId_file
    orderhistory_GetCreditInvoiceDetailForWest_file: Path = ordermanagement_orderhistory_GetCreditInvoiceDetailForWest_file

    def __init__(self):
        # open instance variable json files and store to instance variables
        with open(self.brands_GetProductDetailsFromService_xml_file, 'r') as f:
            self.brands_GetProductDetailsFromService_xml = f.read()
        with open(self.brands_path_GetProductsByFullText_json_file, 'r') as f:
            self.brands_path_GetProductsByFullText_json = json.load(f)
        with open(self.ProductDetail_GetProductDetailByProductIntId_file, 'r') as f:
            self.ProductDetail_GetProductDetailByProductIntId_json = json.load(f)
        with open(self.orderhistory_GetCreditInvoiceDetailForWest_file, 'r') as f:
            self.orderhistory_GetCreditInvoiceDetailForWest = f.read()


