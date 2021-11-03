import os
from typing import Union
from unfi_api import invoice
from unfi_api.api.api import UnfiAPI
from unfi_api.api.order_management import (
    Brands,
    OrderManagement,
    OrderHistory,
    InteractiveReports,
    Categories,
    ProductDetail,
)
from unfi_api.api.products import Products
from unfi_api.product.pricing import Pricing
from unfi_api.api.base_classes import APICore
from unfi_api.product import ProductDetailIntId
from unfi_api.search.result import Result, ProductResult
from unfi_api.api.response import APIResponse, NonJsonResultError
from unfi_api.api.admin_backend import AdminBackend, User, Reports
from unfi_api.invoice import CREDIT, INVOICE, WEB_ORDER, Invoice, OrderList


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
            self._order_management.brands.get_product_pricing_detail(product_code)
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

    def get_invoice_list(self, limit=1000) -> OrderList:
        """
        invoice_id: invoice id
        """
        response: APIResponse = self.order_history.get_invoice_list(
            order_no=None,
            po_no=None,
            req_by=None,
            invoice_no=None,
            page_size=limit,
            page_number=1,
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

    def get_product_result_by_product_code(self, product_code: str) -> Union[ProductResult, None]:
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
        result = ProductDetailIntId.parse_obj(
            self.product_detail.get_product_detail_by_int_id(int_id)
        )
        return result


def main():
    api = UnfiAPI(os.environ["UNFI_USER"], os.environ["UNFI_PASS"], incapsula=False)
    client = UnfiApiClient(api)
    result = client.search("chocolate")
    pass


if __name__ == "__main__":
    main()
