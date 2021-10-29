### unit tests for Attribute and Attributes classes
import json
from pathlib import Path
from unittest import TestCase
from unfi_api_tests.assets import ProductsFiles
from unfi_api.product.attributes import Attribute, Attributes

class TestAttribute(TestCase):
    
    def setUp(self) -> None:
        self.products_files: ProductsFiles = ProductsFiles()
        
    def test_create_attribute_object(self):
        """attempt to create an attribute using a single attribute from the attribute json array
        [{'AttributeID': 22, 'AttributeName': 'Kosher', 'SourceOfAttributeData': 'PWS', 'CreatedBy': 10, 'CreatedDate': '2015-09-05T02:01:08.597', 'ModifiedBy': 10, 'ModifiedDate': '2015-09-05T02:01:08.597', 'Active': '1'}, {'AttributeID': 27, 'AttributeName': 'Natural or Organic Ingredients', 'SourceOfAttributeData': 'PWS', 'CreatedBy': 10, 'CreatedDate': '2015-09-05T02:01:08.597', 'ModifiedBy': 10, 'ModifiedDate': '2015-09-05T02:01:08.597', 'Active': '1'}, {'AttributeID': 31, 'AttributeName': 'Non-GMO Project Verified ', 'SourceOfAttributeData': 'PWS', 'CreatedBy': 10, 'CreatedDate': '2015-09-05T02:01:08.597', 'ModifiedBy': 10, 'ModifiedDate': '2015-09-05T02:01:08.597', 'Active': '1'}]"""
        attribute_json = self.products_files.attributes_json
        single_attribute = attribute_json[0]
        attribute: Attribute = Attribute(**single_attribute)
        self.assertEqual(attribute.attribute_name, single_attribute['AttributeName'])
        self.assertEqual(attribute.attribute_id, single_attribute['AttributeID'])


class TestAttributes(TestCase):


    def setUp(self) -> None:
        self.products_files: ProductsFiles = ProductsFiles()
        
    def test_create_attributes_object(self):
        """
        attempt to create an attributes object using the attributes json array
        """
        attributes_json = self.products_files.attributes_json
        print(attributes_json)
        attributes: Attributes = Attributes.parse_obj(attributes_json)
        self.assertEqual(attributes.count(), len(attributes_json))
        for idx,attribute in enumerate(attributes):
            self.assertEqual(attribute.attribute_name, attributes_json[idx]['AttributeName'])
            self.assertEqual(attribute.attribute_id, attributes_json[idx]['AttributeID'])
        
        # see if all attribute names are in the json array
        for json_attribute in attributes_json:
            self.assertTrue(json_attribute['AttributeName'] in attributes.get_attribute_names())
    
    def test_print_attributes(self):
        """
        attempt to print the attributes object
        """
        attributes_json = self.products_files.attributes_json
        attributes: Attributes = Attributes.parse_obj(attributes_json)
        print(attributes)
        



