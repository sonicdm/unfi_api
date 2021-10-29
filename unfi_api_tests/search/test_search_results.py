from unittest import TestCase
from unfi_api.search.result import Result
from unfi_api_tests.assets import OrderManagementFiles


class TestResult(TestCase):

    def setUp(self) -> None:
        self.order_management_files = OrderManagementFiles()

    def test_result_init(self):
        """test loading result from json api response"""

        result_json = self.order_management_files.brands_path_GetProductsByFullText_json
        self.result = Result(**result_json)
        pass
