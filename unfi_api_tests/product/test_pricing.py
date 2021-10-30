from unfi_api.product.pricing import Cost, Pricing, parse_pricing
from unittest import TestCase
from unfi_api_tests.assets import ProductsFiles, OrderManagementFiles
from datetime import date


class TestCost(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pricing_dict = {
            "case_price": 27.24,
            "unit_price": 4.54,
            "retail_margin": 0.3505,
            "retail_price": 6.99,
            "costs": {
                "R": {
                    "price_type": "R",
                    "price_description": "Retail",
                    "min_qty": 1,
                    "discount_amount": 0.0,
                    "discount_sign": "",
                    "net_flag": "",
                    "case_savings": 0.0,
                    "each_savings": 0.0,
                    "start_date": None,
                    "end_date": None,
                    "case_price": 27.24,
                    "unit_price": 4.54,
                    "retail_price": 6.99,
                    "margin": 0.3505,
                },
                "S": {
                    "price_type": "S",
                    "price_description": "Customer Specific Shelf Sale",
                    "min_qty": 1,
                    "discount_amount": 21.79,
                    "discount_sign": "",
                    "net_flag": "",
                    "case_savings": 5.45,
                    "each_savings": 0.91,
                    "start_date": "09/25/2021",
                    "end_date": "10/29/2021",
                    "case_price": 21.79,
                    "unit_price": 3.63,
                    "retail_price": 6.99,
                    "margin": 0.4804,
                },
            },
        }

    def test_create_retail_cost(self) -> None:
        cost = Cost.parse_obj(self.pricing_dict['costs']["R"])
        self.assertEqual(cost.price_type, "R")
        self.assertEqual(cost.price_description, "Retail")
        self.assertEqual(cost.min_qty, 1)
        self.assertEqual(cost.discount_amount, 0.0)
        self.assertEqual(cost.discount_sign, "")
        self.assertEqual(cost.net_flag, "")
        self.assertEqual(cost.case_savings, 0.0)
        self.assertEqual(cost.each_savings, 0.0)
        self.assertEqual(cost.start_date, None)
        self.assertEqual(cost.end_date, None)
        self.assertEqual(cost.case_price, 27.24)
        self.assertEqual(cost.unit_price, 4.54)
        self.assertEqual(cost.retail_price, 6.99)
        self.assertEqual(cost.margin, 0.3505)

    def test_create_customer_specific_shelf_sale_cost(self) -> None:
        cost = Cost.parse_obj(self.pricing_dict['costs']["S"])
        self.assertEqual(cost.price_type, "S")
        self.assertEqual(cost.price_description, "Customer Specific Shelf Sale")
        self.assertEqual(cost.min_qty, 1)
        self.assertEqual(cost.discount_amount, 21.79)
        self.assertEqual(cost.discount_sign, "")
        self.assertEqual(cost.net_flag, "")
        self.assertEqual(cost.case_savings, 5.45)
        self.assertEqual(cost.each_savings, 0.91)
        self.assertEqual(cost.start_date, date(2021, 9, 25))
        self.assertEqual(cost.end_date, date(2021, 10, 29))
        self.assertEqual(cost.case_price, 21.79)
        self.assertEqual(cost.unit_price, 3.63)
        self.assertEqual(cost.retail_price, 6.99)
        self.assertEqual(cost.margin, 0.4804)


class TestPricing(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pricing_dict = {
            "case_price": 27.24,
            "unit_price": 4.54,
            "retail_margin": 0.3505,
            "retail_price": 6.99,
            "costs": {
                "R": {
                    "price_type": "R",
                    "price_description": "Retail",
                    "min_qty": 1,
                    "discount_amount": 0.0,
                    "discount_sign": "",
                    "net_flag": "",
                    "case_savings": 0.0,
                    "each_savings": 0.0,
                    "start_date": None,
                    "end_date": None,
                    "case_price": 27.24,
                    "unit_price": 4.54,
                    "retail_price": 6.99,
                    "margin": 0.3505,
                },
                "S": {
                    "price_type": "S",
                    "price_description": "Customer Specific Shelf Sale",
                    "min_qty": 1,
                    "discount_amount": 21.79,
                    "discount_sign": "",
                    "net_flag": "",
                    "case_savings": 5.45,
                    "each_savings": 0.91,
                    "start_date": "09/25/2021",
                    "end_date": "10/29/2021",
                    "case_price": 21.79,
                    "unit_price": 3.63,
                    "retail_price": 6.99,
                    "margin": 0.4804,
                },
            },
        }
    def test_create_pricing(self) -> None:
        pricing = Pricing.parse_obj(self.pricing_dict)
        self.assertEqual(pricing.case_price, 27.24)
        self.assertEqual(pricing.unit_price, 4.54)
        self.assertEqual(pricing.retail_margin, 0.3505)
        self.assertEqual(pricing.retail_price, 6.99)
        self.assertIn("R", pricing.costs)
        self.assertIn("S", pricing.costs)


class TestPriceParsing(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.product_files = ProductsFiles()
        cls.ordermanagement_files = OrderManagementFiles()

    def test_price_parsing(self):
        costs_xml = self.ordermanagement_files.brands_GetProductDetailsFromService_xml
        parsed_pricing = parse_pricing(costs_xml)
        pass
