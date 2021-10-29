import pathlib

### Asset File Information ###
# base directory paths
thisfiledir = pathlib.Path(__file__).parent
assets_path = pathlib.Path(thisfiledir, 'assets')
# asset subdirectories
products_dir = pathlib.Path(assets_path, 'products')
ordermanagement_path = pathlib.Path(assets_path, 'ordermanagement')

# ordermanagement sub directories
ordermanagement_brands_dir = pathlib.Path(ordermanagement_path, 'brands')
ordermanagement_ProductDetail_dir = pathlib.Path(ordermanagement_path, 'ProductDetail')

# ordermanagement brands files
ordermanagement_brands_GetProductDetailsFromService_xml_file = pathlib.Path(ordermanagement_brands_dir, 'GetProductDetailsFromService.xml')
ordermanagement_brands_path_GetProductsByFullText_json_file = pathlib.Path(ordermanagement_brands_dir, 'GetProductsByFullText.json')

# ordermanagement ProductDetail files
ordermanagement_ProductDetail_GetProductDetailByProductIntId_file = pathlib.Path(ordermanagement_ProductDetail_dir, 'GetProductDetailByProductIntId.json')

# products subdirectories
products_products_dir = pathlib.Path(products_dir, 'products')

# products files
products_GetWestProductData_json_file = pathlib.Path(products_products_dir, 'GetWestProductData.json')
int_id_json_file = pathlib.Path(products_products_dir, "int_id.json")

# int_id directory
int_id_dir = pathlib.Path(products_products_dir, 'int_id')

# int_id directory json files
nutrition_json_file = pathlib.Path(int_id_dir, 'nutrition.json')
attributes_json_file = pathlib.Path(int_id_dir, 'attributes.json')
marketing_json_file = pathlib.Path(int_id_dir, 'marketing.json')
ingredients_json_file = pathlib.Path(int_id_dir, 'ingredients.json')