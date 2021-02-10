from unittest import TestCase
import json
from unfi_api import products
from unfi_api.api.order_management.brands import parse_pricing_table
from os import path
import pathlib
import codecs

thisfiledir = pathlib.Path(__file__).parent.absolute()


class Test(TestCase):

    @classmethod
    def setUpClass(cls):
        with open(path.join(thisfiledir, r"assets\products\products\attributes.json"), "r") as attributes:
            cls.products_products_attributes = json.load(attributes)
        with open(path.join(thisfiledir, r"assets\products\products\ingredients.json"), "r") as ingredients:
            cls.products_products_ingredients = json.load(ingredients)
        with open(path.join(thisfiledir, r"assets\products\products\marketing.json"), "r") as marketing:
            cls.products_products_marketing = json.load(marketing)
        with open(path.join(thisfiledir, r"assets\products\products\nutrition.json"), "r") as nutrition:
            cls.products_products_nutrition = json.load(nutrition)
        with open(path.join(thisfiledir, r"assets\products\products\product.json"), "r") as product:
            cls.products_products_product = json.load(product)
        with open(
                path.join(thisfiledir, r"assets\products\products\GetWestProductData.json"), "r"
        ) as GetWestProductData:
            cls.products_products_GetWestProductData = json.load(GetWestProductData)
        # pricing table
        with codecs.open(
                path.join(thisfiledir, "assets/ordermanagement/brands/GetProductDetailsFromService.html"), "r", "utf-8"
        ) as GetProductDetailsFromService:
            page = str(GetProductDetailsFromService.read())
            cls.product_pricing = parse_pricing_table(page)
        with open(
                r"assets\ordermanagement\productdetail\GetProductDetailByProductIntId.json") as GetProductDetailByProductIntId:
            cls.ordermanagement_productdetail_get_product_detail_by_int_id = json.load(GetProductDetailByProductIntId)

    def test_product(self):
        product = products.Product(
            product=self.products_products_product,
            product_data=self.products_products_GetWestProductData,
            product_detail=self.ordermanagement_productdetail_get_product_detail_by_int_id[0],
            marketing=self.products_products_marketing,
            ingredients=self.products_products_ingredients,
            nutrition_facts=self.products_products_nutrition,
            attributes=self.products_products_attributes,
            pricing=self.product_pricing
        )
        pass

    def test_pricing(self):
        pricing = products.Pricing(self.product_pricing)
        pass

    def test_cost(self):
        cost = products.Cost(**self.product_pricing[0])
        print("Cost: " + str(cost))

    def test_attribute(self):
        self.fail()

    def test_marketing(self):
        marketing = products.Marketing(**self.products_products_marketing)
        pass

    def test_nutrition_facts(self):
        nutrition_facts = products.NutritionFacts(self.products_products_nutrition)
        pass

    def test_ingredients(self):
        self.fail()
