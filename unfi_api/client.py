from __future__ import annotations

import concurrent.futures.thread
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Dict, List, Union

from unfi_api.api.admin_backend import AdminBackend, Reports, User
from unfi_api.api.api import UnfiAPI
from unfi_api.api.base_classes import APICore
from unfi_api.api.order_management import (
    Brands,
    Categories,
    InteractiveReports,
    OrderHistory,
    OrderManagement,
    ProductDetail,
)
from unfi_api.api.products import Products
from unfi_api.api.response import APIResponse, NonJsonResultError
from unfi_api.download import download_products, download_invoices
from unfi_api.invoice import (
    CREDIT,
    INVOICE,
    WEB_ORDER,
    Invoice,
    OrderList,
    OrderListing,
)
from unfi_api.product import (
    Attributes,
    Ingredients,
    Marketing,
    NutritionFacts,
    Pricing,
    ProductData,
    ProductDetailIntId,
    ProductIntID,
    UNFIProduct,
    UNFIProducts,
)
from unfi_api.search.result import ProductResult, Result, Results
from unfi_api.utils.threading import threader


class UnfiApiClient:
    def __init__(self, api: APICore):
        self.api: UnfiAPI = api
        self.user = User(api)
        self.brands = Brands(api)
        self.reports = Reports(api)
        self.products = Products(api)
        self.categories = Categories(api)
        self.order_history = OrderHistory(api)
        self.admin_backend = AdminBackend(api)
        self.product_detail = ProductDetail(api)
        self.order_management = OrderManagement(api)
        self.interactive_reports = InteractiveReports(api)

    @property
    def auth_token(self) -> str:
        return self.api.auth_token

    def search(
        self,
        query,
        limit=1000,
        organic_codes="",
        attribute_ids="",
        sales_filters="",
        brand_ids="",
        category_ids="",
        page_number=1,
    ):

        result = self.brands.get_products_by_full_text(
            query,
            limit,
            organic_codes,
            attribute_ids,
            sales_filters,
            brand_ids,
            category_ids,
            page_number,
        )
        res = Result.parse_obj(result["data"])
        return res

    def get_pricing(self, product_code: str) -> Pricing:
        """
        product code: 5 digit unique product code
        """
        response: APIResponse = (
            self.order_management.brands.get_product_pricing_detail(product_code)
        )
        if not response.data:
            raise NonJsonResultError(
                f"Non-JSON API response for product code {product_code}"
            )
        res = Pricing.parse_obj(response.data)
        return res

    def get_invoice(self, invoice_number: str) -> Invoice:
        """
        invoice_id: invoice id
        """
        response: APIResponse = self.order_history.get_invoice(invoice_number)
        if not response.content_type == "application/json" or not response.data:
            raise NonJsonResultError(
                f"Non-JSON API data for invoice number {invoice_number}"
            )
        return Invoice.parse_obj(response.data)

    def get_invoices(
        self,
        order_list: Union[OrderList, List[str], List[OrderListing]],
        callback: Callable = None,
        threaded=False,
        thread_count=4,
        get_results=True,
    ) -> Union[List[Invoice],None]:
        orders: List[Invoice] = []
        invoice_numbers = []
        for order in order_list:
            if isinstance(order, OrderListing):
                invoice_numbers.append(order.invoice_number)
            elif isinstance(order, str):
                invoice_numbers.append(order)
            else:
                raise ValueError(
                    f"order_list must be a list of OrderListing or strings got {type(order)} instead."
                )
        orders = download_invoices(
            self,
            invoice_numbers,
            callback=callback,
            threaded=threaded,
            thread_count=thread_count,
        )
        return orders

    def get_invoice_list(self, limit=1000, page_number=1) -> OrderList:
        """
        invoice_id: invoice id
        """
        response: APIResponse = self.order_history.get_invoice_list(
            order_no=None,
            po_no=None,
            req_by=None,
            invoice_no=None,
            page_size=limit,
            page_number=page_number,
            sort_expression=None,
            sort_direction=None,
        )
        if not response.content_type == "application/json" or not response.data:
            raise NonJsonResultError(f"Non-JSON API response for invoice list request")
        return OrderList.parse_obj(response.data)

    def get_credit_list(self, invoice_id: str, type: str) -> OrderList:
        """
        invoice_id: invoice id
        """
        response: APIResponse = self.order_history.get_credit_list()
        if not response.content_type == "application/json" or not response.data:
            raise NonJsonResultError(f"Non-JSON API response for credit list request")
        return OrderList.parse_obj(response.data)

    def get_product_result_by_product_code(
        self, product_code: str
    ) -> Union[ProductResult, None]:
        """
        product_code: 5 digit unique product code
        this is slow because the only way to get the other information for pulling a product is to search for it and get the listing.
        """
        result = Result.parse_obj(self.search(product_code))
        product = result.get_product_by_product_code(product_code)
        if not product:
            return None
        return product

    def get_product_detail_by_int_id(self, int_id: str) -> Union[ProductResult, None]:
        """
        int_id: internal product id
        """
        response = self.product_detail.get_product_detail_by_int_id(int_id)
        if not response.data or not response.content_type == "application/json":
            raise NonJsonResultError(
                f"Non-JSON API response for product detail request"
            )
        result = ProductDetailIntId.parse_obj(response.data)
        return result

    def get_product_int_id(self, int_id) -> APIResponse:
        result = self.products.get_product_by_int_id(int_id)
        return result

    def get_product_attributes(self, int_id) -> Attributes:
        result = self.products.get_product_attributes_by_int_id(int_id)
        attributes = Attributes.parse_obj(result.data)
        return attributes

    def get_product_data(self, product_code: str) -> ProductData:
        result = self.products.get_west_product_data(product_code)
        product_data = ProductData.parse_obj(result.data)
        return product_data

    def get_product_nutrition(self, int_id: str) -> NutritionFacts:
        result = self.products.get_product_nutrition_by_int_id(int_id)
        if not result.data:
            return None
        product_nutrition = NutritionFacts.parse_obj(result.data)
        return product_nutrition

    def get_product_marketing(self, int_id: str) -> Marketing:
        result = self.products.get_product_marketing_by_int_id(int_id)
        product_marketing = Marketing.parse_obj(result.data)
        return product_marketing

    def get_product_ingredients(self, int_id: str) -> Ingredients:
        result = self.products.get_product_ingredients_by_int_id(int_id)
        if result.data:
            return Ingredients.parse_obj(result.data)
        return None

    def get_product_image(self, int_id: str) -> Union[bytes, None]:
        result = self.products.get_product_image(int_id)
        if not result["error"] and result["data"]:
            return result["data"]
        return None

    def get_product_pricing(self, product_code) -> Pricing:
        result = self.brands.get_product_pricing_detail(product_code)
        product_pricing = Pricing.parse_obj(result.data)
        return product_pricing

    def get_product(self, product_result: ProductResult) -> UNFIProduct:
        """
        product_result: ProductResult
        """
        int_id = product_result.product_int_id
        product_code = product_result.product_code
        product_detail_by_int_id = self.get_product_detail_by_int_id(int_id)
        west_product_data = self.get_product_data(product_code)
        ingredients = self.get_product_ingredients(int_id)
        nutrition = self.get_product_nutrition(int_id)
        marketing = self.get_product_marketing(int_id)
        pricing = self.get_product_pricing(product_code)
        pricing_info = pricing.costs_to_dict()
        attributes = self.get_product_attributes(int_id)
        attributes_info = attributes.get_attribute_flags()
        product_by_int_id = self.get_product_int_id(int_id)
        product_int_id = ProductIntID.parse_obj(product_by_int_id.data)
        product = UNFIProduct(
            data_by_int_id=product_detail_by_int_id,
            data=west_product_data,
            marketing=marketing,
            pricing=pricing,
            attributes=attributes,
            listing=product_result,
            nutrition=nutrition,
            ingredients=ingredients,
            int_id=product_int_id,
        )
        return product

    def get_products(
        self,
        result: Union[Result, List[ProductResult]],
        callback: Callable = None,
        threaded: bool=False,
        thread_count: int=4,
        job_id:str=None,
    ) -> UNFIProducts:
        """
        product_list: OrderList
        """
        products: Dict[str, UNFIProduct] = {}
        if isinstance(result, (Result, Results)):
            results = result.product_results
        elif isinstance(result, list):
            results = result
        products = download_products(
            self,
            results,
            callback,
            threaded=threaded,
            thread_count=thread_count,
            job_id=job_id,
        )
        return products

    def set_account(self, account_id: str):
        self.user.insert_selected_account_as_default(account_id)
