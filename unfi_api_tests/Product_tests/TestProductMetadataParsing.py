import unittest
import json
from pathlib import Path
from unfi_api.old_product import get_attributes, parse_attributes, parse_pricing
from unfi_api.products import *
import os


class TestGet_attributes(unittest.TestCase):

    def setUp(self) -> None:
        self.assets_path = Path("../assets/")

    def test_parse_attributes(self):
        # example of a json result from the api
        test_result = [
            {'AttributeID': 22, 'AttributeName': 'Kosher', 'SourceOfAttributeData': 'PWS', 'CreatedBy': 10,
             'CreatedDate': '2015-09-05T02:01:08.597', 'ModifiedBy': 10,
             'ModifiedDate': '2015-09-05T02:01:08.597', 'Active': '1'},
            {'AttributeID': 27, 'AttributeName': 'Natural or Organic Ingredients', 'SourceOfAttributeData': 'PWS',
             'CreatedBy': 10, 'CreatedDate': '2015-09-05T02:01:08.597', 'ModifiedBy': 10,
             'ModifiedDate': '2015-09-05T02:01:08.597', 'Active': '1'},
            {'AttributeID': 38, 'AttributeName': 'Specialty Product', 'SourceOfAttributeData': 'PWS',
             'CreatedBy': 10, 'CreatedDate': '2015-09-05T02:01:08.597', 'ModifiedBy': 10,
             'ModifiedDate': '2015-09-05T02:01:08.597', 'Active': '1'}
        ]
        expected_output = {'Kosher': 'Y', 'Natural or Organic Ingredients': 'Y', 'Specialty Product': 'Y'}
        result = parse_attributes(test_result)
        self.assertEqual(result, expected_output)

    def test_parse_pricing(self):
        with open('pricing_sample_html.html', 'r') as page_html:
            page = page_html.read()
        parse_pricing(page)

    def test_parse_nutrients(self):
        nutrient_json_path = "../assets/products/products/nutrition.json"
        nutrients = []
        with open(nutrient_json_path, "r") as nutrition_facts_json:
            nutrition_facts = json.load(nutrition_facts_json)
        for nutrient in nutrition_facts:
            nutrient_obj = Nutrient(**nutrient)
            nutrients.append(nutrient_obj)
        pass

    def test_nutrition_facts(self):
        nutrition_facts_json_path = self.assets_path.joinpath("products/products/nutrition.json")
        with nutrition_facts_json_path.open('r') as fh:
            nutrition_facts_json = json.load(fh)
        nutrition_facts = NutritionFacts(nutrition_facts_json)
        pass
