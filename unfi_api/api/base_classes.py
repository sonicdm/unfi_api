


class Endpoint:
    """Base for API Endpoint"""


class APICore:
    """Base for API Object"""

    ordermanagement: Endpoint
    products: Endpoint
    brands: Endpoint
    categories: Endpoint
    interactive_reports: Endpoint
    order_history: Endpoint
    product_detail: Endpoint

        