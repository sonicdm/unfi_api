from unfi_api import invoice
from unfi_api.api.api import UnfiAPI
from unfi_api.api.base_classes import APICore
from unfi_api.api.response import APIResponse, NonJsonResultError
from unfi_api.search.result import Result
from unfi_api.product.pricing import Pricing
from unfi_api.invoice import CREDIT, INVOICE, WEB_ORDER, Invoice, OrderList
from unfi_api.api.order_management import Brands, OrderManagement, OrderHistory, InteractiveReports, Categories, ProductDetail
from unfi_api.api.admin_backend import AdminBackend, User, Reports
from unfi_api.api.products import Products


class UnfiApiClient:
    def __init__(self, api: APICore):
        self.api = api
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


    def search(self, query, limit=1000, organic_codes="", attribute_ids="", sales_filters="", brand_ids="", category_ids="", page_number=1):
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

    def get_invoice(self, invoice_number: str) -> APIResponse:
        """
        invoice_id: invoice id
        """
        response: APIResponse = self.order_history.get_invoice(invoice_number)
        if not response.content_type == "application/json" or not response.data:
            raise NonJsonResultError(f"Non-JSON API data for invoice number {invoice_number}")
        return Invoice.parse_obj(response.data)
    
    def get_invoice_list(self) -> Invoice:
        """
        invoice_id: invoice id
        """
        response: APIResponse = self.order_history.get_invoice_list(order_no=None, po_no=None, req_by=None, invoice_no=None,
                         page_size=1000, page_number=1, sort_expression=None, sort_direction=None)
        if not response.content_type == "application/json" or not response.data:
            raise NonJsonResultError(f"Non-JSON API response for invoice id {invoice_id}")
        return OrderList.parse_obj(response.data)
    
    def get_credit_list(self, invoice_id: str, type: str) -> Invoice:
        """
        invoice_id: invoice id
        """
        response: APIResponse = self.order_history.get_credit_list(invoice_id)
        if not response.content_type == "application/json" or not response.data:
            raise NonJsonResultError(f"Non-JSON API response for invoice id {invoice_id}")
        return response


def main():
    client = UnfiApiClient("capellaAPI", "CapellaAPI2489", incapsula=False)
    result = client.search("chocolate")
    pass


if __name__ == "__main__":
    main()
