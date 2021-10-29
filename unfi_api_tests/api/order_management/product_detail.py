from unittest import TestCase
from unfi_api import UnfiAPI

user = "Scanning@capellamarket.com"
password = "CapellaPOS2489"


class TestProductDetail(TestCase):
    def test_get_product_detail_by_int_id(self):
        api = UnfiAPI(user, password)
        detail = api.order_management.product_detail.get_product_detail_by_int_id(207555)
        pass
