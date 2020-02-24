import unittest
from unfi_api.Product import get_attributes, parse_attributes, parse_pricing
import os


class TestGet_attributes(unittest.TestCase):

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
