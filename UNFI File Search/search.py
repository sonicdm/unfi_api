import os
from typing import List
from unfi_api import UnfiApiClient, UnfiAPI
from unfi_api.search.result import ProductResult, Result
from unfi_api.utils.collections import lower_case_keys


def main():
    user = os.environ.get("UNFI_USER")
    password = os.environ.get("UNFI_PASSWORD")
    api = UnfiAPI(user, password)
    client = UnfiApiClient(api)

def search_files(client, query):
    """
    Search for files in the Unifi File Search API.
    """
    return client.search_files(query)


def download_search_products(client: UnfiApiClient, result: Result):
    """
    Get the search results from the Unifi File Search API.
    """
    products = []
    top_products: List[ProductResult] = result.products
    for product in top_products:
        product_data = {}
       
        int_id = product.product_int_id
        product_code = product.product_code
        product_by_int_id = client.get_product_detail_by_int_id(int_id)
        west_product_data = client.get_product_data(product_code)
        marketing = client.get_product_marketing(int_id)
        pricing = client.get_product_pricing(product_code)
        pricing_info = pricing.costs_to_dict()
        attributes = client.get_product_attributes(int_id)
        attributes_info = attributes.attributes()
        product_data.update(west_product_data.dict())
        product_data.update(pricing_info)
        product_data.update(attributes_info)
        product_data.update(marketing.dict())
        product_data.update(product.dict())
        product_data.update(product_by_int_id.dict())
        products.append(lower_case_keys(product_data))




if __name__ == "__main__":
    main()