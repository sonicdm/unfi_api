import codecs
import json
import pathlib
from os import path
from unittest import TestCase
from devtools import debug
from unfi_api import product
from typing import List, Dict, Any
import unfi_api.product.ingredients
import unfi_api.product.nutrition
import unfi_api.product.pricing
from dateutil.parser import parse as date_parse

from unfi_api.api.order_management.brands import parse_pricing_table
from unfi_api.product.pricing import Cost, Costs
from unfi_api.search.result import Result
from unfi_api_tests.assets import ProductsFiles, OrderManagementFiles
from unfi_api.product.attributes import Attributes, Attribute
from unfi_api.product.ingredients import Ingredients
from unfi_api.product.nutrition import NutritionFacts, Nutrient
from unfi_api.product.marketing import Marketing
from unfi_api.product import ProductData
from unfi_api.product import ProductDetailIntId
from unfi_api.product import ProductListing


class TestProductData(TestCase):

    @classmethod
    def setUpClass(cls):
        """ Set up class for testing
        """
        # read in json files
        cls.product_files = ProductsFiles()

    def test_product_data(self):
        """ Test product data object and make sure it matches the input json with the object property alias
        """
        input_json = {
            "productID": "08345",
            "effectiveDate": "05/25/2020",
            "status": "Manufacturer Outage - Expect Delays",
            "netPrice": "32.0000",
            "retailPrice": "3.69",
            "priceReason": "Regular Price",
            "margin": "27.73",
            "stockOh": "0",
            "stockAvail": "-142",
            "allow": "Y",
            "refersTo": "TestRefersTo",
            "buyerNotes": "TestBuyerNotes",
            "buyerCode": "T2"
        }

        product_data = ProductData.parse_obj(input_json)
        object_values = product_data.dict(by_alias=True)
        # check that each value matches the input json if it exists in the json
        self.assertEqual(input_json["productID"], object_values["productID"])
        self.assertEqual(
            input_json["effectiveDate"], object_values["effectiveDate"].strftime("%m/%d/%Y"))
        self.assertEqual(input_json["status"], object_values["status"])
        self.assertEqual(
            float(input_json["netPrice"]), object_values["netPrice"])
        self.assertEqual(
            float(input_json["retailPrice"]), object_values["retailPrice"])
        self.assertEqual(input_json["priceReason"],
                         object_values["priceReason"])
        self.assertEqual(
            float(input_json["margin"]) / 100, object_values["margin"])
        self.assertEqual(int(input_json["stockOh"]), object_values["stockOh"])
        self.assertEqual(
            int(input_json["stockAvail"]), object_values["stockAvail"])
        self.assertEqual(input_json["allow"], object_values["allow"])
        self.assertEqual(input_json["refersTo"], object_values["refersTo"])
        self.assertEqual(input_json["buyerNotes"], object_values["buyerNotes"])
        self.assertEqual(input_json["buyerCode"], object_values["buyerCode"])


class TestProductDetail(TestCase):

    def test_product_detail(self):
        """ Test product detail object and make sure it matches the input json with the object property alias
        """
        raw_input_json = """{
        "StockAvail": 70,
        "StockOH": 70,
        "PerUnitPrice": 40.25,
        "BrandId": 15432,
        "BrandName": "FIELD DAY",
        "ProductIntID": 400233,
        "ProductCode": "49456",
        "ProductName": "Cereal, Golden Rice Crisps",
        "Discount": "S",
        "UPC": "042563-602918",
        "PackSize": "14/12 OZ",
        "Price": 40.25,
        "UnitsInFullCase": 14,
        "MINQTY": 0,
        "InnerCaseUPC": "00000000000000",
        "MasterCaseUPC": "20042563602912",
        "PLU": null,
        "PVLabelCode": "0",
        "MemberApplicableFee": 0.00,
        "OrganicCode": "OG2",
        "SubHeader": "",
        "CategoryID": 353,
        "CategoryName": "GROCERY - CEREAL - COLD",
        "CountryOfOriginID": 253,
        "CountryOfOriginName": "USA, RHODE ISLAND",
        "WarehouseMessage": null,
        "IsNew": false
        }"""

        product_detail = ProductDetailIntId.parse_raw(raw_input_json)
        object_values = product_detail.dict(by_alias=True)
        input_json = json.loads(raw_input_json)
        # check that each value matches the input json if it exists in the json
        object_dict = product_detail.dict(by_alias=True)
        self.assertEqual(
            int(input_json["StockAvail"]), object_dict["StockAvail"])
        self.assertEqual(int(input_json["StockOH"]), object_dict["StockOH"])
        self.assertEqual(
            float(input_json["PerUnitPrice"]), object_dict["PerUnitPrice"])
        self.assertEqual(int(input_json["BrandId"]), object_dict["BrandId"])
        self.assertEqual(input_json["BrandName"], object_dict["BrandName"])
        self.assertEqual(
            int(input_json["ProductIntID"]), object_dict["ProductIntID"])
        self.assertEqual(input_json["ProductCode"], object_dict["ProductCode"])
        self.assertEqual(input_json["ProductName"], object_dict["ProductName"])
        self.assertEqual(input_json["Discount"], object_dict["Discount"])
        self.assertEqual(
            int(input_json["UPC"].replace("-", "")), object_dict["UPC"])
        self.assertEqual(input_json["PackSize"], object_dict["PackSize"])
        self.assertEqual(float(input_json["Price"]), object_dict["Price"])
        self.assertEqual(
            int(input_json["UnitsInFullCase"]), object_dict["UnitsInFullCase"])
        self.assertEqual(int(input_json["MINQTY"]), object_dict["MINQTY"])
        self.assertEqual(int(input_json["InnerCaseUPC"].replace(
            "-", "")), object_dict["InnerCaseUPC"])
        self.assertEqual(int(input_json["MasterCaseUPC"].replace(
            "-", "")), object_dict["MasterCaseUPC"])
        self.assertEqual(input_json["PLU"], object_dict["PLU"])
        self.assertEqual(input_json["PVLabelCode"], object_dict["PVLabelCode"])
        self.assertEqual(
            float(input_json["MemberApplicableFee"]), object_dict["MemberApplicableFee"])
        self.assertEqual(input_json["OrganicCode"], object_dict["OrganicCode"])
        self.assertEqual(input_json["SubHeader"], object_dict["SubHeader"])
        self.assertEqual(
            int(input_json["CategoryID"]), object_dict["CategoryID"])
        self.assertEqual(input_json["CategoryName"],
                         object_dict["CategoryName"])
        self.assertEqual(
            int(input_json["CountryOfOriginID"]), object_dict["CountryOfOriginID"])
        self.assertEqual(input_json["CountryOfOriginName"],
                         object_dict["CountryOfOriginName"])
        self.assertEqual(input_json["WarehouseMessage"],
                         object_dict["WarehouseMessage"])
        self.assertEqual(input_json["IsNew"], object_dict["IsNew"])


class TestProductListing(TestCase):
    def test_create_product_listing(self):
        """ Test product listing object and make sure it matches the input json with the object property alias
        """
        raw_json = r"""{
    "ProductIntID": 412029,
    "DivisionCode": "WEST",
    "ProductNumber": "46712",
    "ProductName": "Tortillas Burrito Size",
    "CategoryID": 367,
    "BrandID": 16627,
    "SubHeaderID": 36796,
    "DepartmentID": 13,
    "UPC": "00865336000083",
    "InnerCaseUPC": "00000000000000",
    "MasterCaseUPC": "10865336000080",
    "PLU": null,
    "OrganicCode": "",
    "SpecialityFlag": "2",
    "CountryOfOriginID": 257,
    "IsPrivateLabel": "0",
    "ProductOwner": "WBS",
    "Ingredients": "Grain Free Burrito Tortilla Wrap Cassava Flour, Water, Coconut Flour, Tapioca Flour, Arrowroot Flour, Avocado Oil, Apple Cider Vinegar, Sea Salt, Yeast.  \r\n",
    "ImgFileName": "\\\\CTDAYNPF081\\Images\\PHOTO ARCHIVE\\Grocery\\S (grocery)\\Siete\\252188c TORTILLA,BURRITO SIZE  15 OZ\\252188ccw.jpg",
    "ImgUrl": null,
    "IsImageAvailable": true,
    "MinimumOrderQuantity": 0,
    "SubstituteNumber": null,
    "ShortDescription": "TORTILLA,BURRITO SIZE                                       ",
    "LongDescription": null,
    "SearchKeywords": null,
    "PackSize": "6/15 OZ",
    "UnitsInFullCase": 6,
    "UnitType": null,
    "Size": null,
    "CreatedBy": 10,
    "CreatedDate": "2019-11-08T09:05:49.57",
    "ModifiedBy": 10,
    "ModifiedDate": "2020-05-22T09:05:21.35",
    "IsActive": true,
    "IsDeleted": false,
    "PrivateLblDept": 0,
    "RequiresCustomerAuthorization": false
    }"""
        input_json = json.loads(raw_json, strict=False)
        product_listing = ProductListing.parse_raw(raw_json)
        object_values = product_listing.dict(by_alias=True)
        # check that each value matches the input json if it exists in the json
        object_dict = product_listing.dict(by_alias=True)
        self.assertEqual(
            int(input_json["ProductIntID"]), object_dict["ProductIntID"])
        self.assertEqual(input_json["DivisionCode"],
                         object_dict["DivisionCode"])
        self.assertEqual(input_json["ProductNumber"],
                         object_dict["ProductNumber"])
        self.assertEqual(input_json["ProductName"], object_dict["ProductName"])
        self.assertEqual(
            int(input_json["CategoryID"]), object_dict["CategoryID"])
        self.assertEqual(int(input_json["BrandID"]), object_dict["BrandID"])
        self.assertEqual(
            int(input_json["SubHeaderID"]), object_dict["SubHeaderID"])
        self.assertEqual(
            int(input_json["DepartmentID"]), object_dict["DepartmentID"])
        self.assertEqual(
            int(input_json["UPC"].replace("-", "")), object_dict["UPC"])
        self.assertEqual(int(input_json["InnerCaseUPC"].replace(
            "-", "")), object_dict["InnerCaseUPC"])
        self.assertEqual(int(input_json["MasterCaseUPC"].replace(
            "-", "")), object_dict["MasterCaseUPC"])
        self.assertEqual(input_json["PLU"], object_dict["PLU"])
        self.assertEqual(input_json["OrganicCode"], object_dict["OrganicCode"])
        self.assertEqual(input_json["SpecialityFlag"],
                         object_dict["SpecialityFlag"])
        self.assertEqual(
            int(input_json["CountryOfOriginID"]), object_dict["CountryOfOriginID"])
        self.assertEqual(input_json["IsPrivateLabel"],
                         object_dict["IsPrivateLabel"])
        self.assertEqual(input_json["ProductOwner"],
                         object_dict["ProductOwner"])
        self.assertEqual(input_json["Ingredients"], object_dict["Ingredients"])
        self.assertEqual(input_json["ImgFileName"], object_dict["ImgFileName"])
        self.assertEqual(input_json["ImgUrl"], object_dict["ImgUrl"])
        self.assertEqual(input_json["IsImageAvailable"],
                         object_dict["IsImageAvailable"])
        self.assertEqual(
            int(input_json["MinimumOrderQuantity"]), object_dict["MinimumOrderQuantity"])
        self.assertEqual(input_json["SubstituteNumber"],
                         object_dict["SubstituteNumber"])
        self.assertEqual(input_json["ShortDescription"],
                         object_dict["ShortDescription"])
        self.assertEqual(input_json["LongDescription"],
                         object_dict["LongDescription"])
        self.assertEqual(input_json["SearchKeywords"],
                         object_dict["SearchKeywords"])
        self.assertEqual(input_json["PackSize"], object_dict["PackSize"])
        self.assertEqual(
            int(input_json["UnitsInFullCase"]), object_dict["UnitsInFullCase"])
        self.assertEqual(input_json["UnitType"], object_dict["UnitType"])
        self.assertEqual(input_json["Size"], object_dict["Size"])
        self.assertEqual(
            int(input_json["CreatedBy"]), object_dict["CreatedBy"])
        self.assertEqual(date_parse(
            input_json["CreatedDate"]), object_dict["CreatedDate"])
        self.assertEqual(
            int(input_json["ModifiedBy"]), object_dict["ModifiedBy"])
        self.assertEqual(date_parse(
            input_json["ModifiedDate"]), object_dict["ModifiedDate"])
        self.assertEqual(input_json["IsActive"], object_dict["IsActive"])
        self.assertEqual(input_json["IsDeleted"], object_dict["IsDeleted"])
        self.assertEqual(
            int(input_json["PrivateLblDept"]), object_dict["PrivateLblDept"])
        self.assertEqual(input_json["RequiresCustomerAuthorization"],
                         object_dict["RequiresCustomerAuthorization"])


class TestPricing(TestCase):

    @classmethod
    def setUp(cls) -> None:
        # pricing table
        cls.ordermanagement_files = OrderManagementFiles()

    def test_pricing(self):
        pricing_xml = self.ordermanagement_files.brands_GetProductDetailsFromService_xml
        parsed_pricing = parse_pricing_table(pricing_xml)
        pricing = product.Costs(pricing_xml)

    def test_cost(self):
        pricing_xml = self.ordermanagement_files.brands_GetProductDetailsFromService_xml
        parsed_pricing = parse_pricing_table(pricing_xml)
        cost = unfi_api.product.pricing.Cost(**parsed_pricing[0])
        print("Cost: " + str(cost))


class TestOtherAttributes(TestCase):

    @classmethod
    def setUp(cls) -> None:
        cls.products_files = ProductsFiles()

    def test_single_attribute(self):
        attributes_json = self.products_files.attributes_json
        print(attributes_json[0])
        attribute = Attribute.parse_obj(attributes_json[0])
        pass

    def test_attributes(self):
        attributes = Attributes.parse_obj(self.products_files.attributes_json)
        pass


class TestNutritionFacts(TestCase):
    def setUp(self) -> None:
        self.products_files = ProductsFiles()

    def test_nutrition_fact(self):
        nutrition_json = self.products_files.nutrition_json
        nutrition_fact = Nutrient(**nutrition_json[0])
        print(nutrition_fact)

    def test_nutrition_facts(self):
        nutrition_json: List[dict] = self.products_files.nutrition_json
        nutrition_facts = NutritionFacts.parse_obj(
            {"nutrients": nutrition_json})

    def test_nutrition_facts_property(self):
        nutrition_json: List[dict] = self.products_files.nutrition_json
        nutrition_facts = NutritionFacts.parse_obj(
            {"nutrients": nutrition_json})
        print(nutrition_facts.nutrition_facts)

    def test_print_nutrition_facts_as_table(self):
        nutrition_json: List[dict] = self.products_files.nutrition_json
        nutrition_facts = NutritionFacts.parse_obj(
            {"nutrients": nutrition_json})
        print(nutrition_facts.as_table())


class TestIngredients(TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.products_files = ProductsFiles()

    def test_ingredient(self):
        ingredients_json = self.products_files.ingredients_json

        ingredients = Ingredients.parse_obj(ingredients_json)
        pass


class TestProduct(TestCase):

    @classmethod
    def setUpClass(cls):
        # product data assets
        cls.products_files = ProductsFiles()
        cls.ordermanagement_files = OrderManagementFiles()
        cls.product_details_json = r"""{ "ProductIntID": 412029, "DivisionCode": "WEST", "ProductNumber": "46712", "ProductName": "Tortillas Burrito Size", "CategoryID": 367, "BrandID": 16627, "SubHeaderID": 36796, "DepartmentID": 13, "UPC": "00865336000083", "InnerCaseUPC": "00000000000000", "MasterCaseUPC": "10865336000080", "PLU": null, "OrganicCode": "", "SpecialityFlag": "2", "CountryOfOriginID": 257, "IsPrivateLabel": "0", "ProductOwner": "WBS", "Ingredients": "Grain Free Burrito Tortilla Wrap Cassava Flour, Water, Coconut Flour, Tapioca Flour, Arrowroot Flour, Avocado Oil, Apple Cider Vinegar, Sea Salt, Yeast.  \r\n", "ImgFileName": "\\\\CTDAYNPF081\\Images\\PHOTO ARCHIVE\\Grocery\\S (grocery)\\Siete\\252188c TORTILLA,BURRITO SIZE  15 OZ\\252188ccw.jpg", "ImgUrl": null, "IsImageAvailable": true, "MinimumOrderQuantity": 0, "SubstituteNumber": null, "ShortDescription": "TORTILLA,BURRITO SIZE                                       ", "LongDescription": null, "SearchKeywords": null, "PackSize": "6/15 OZ", "UnitsInFullCase": 6, "UnitType": null, "Size": null, "CreatedBy": 10, "CreatedDate": "2019-11-08T09:05:49.57", "ModifiedBy": 10, "ModifiedDate": "2020-05-22T09:05:21.35", "IsActive": true, "IsDeleted": false, "PrivateLblDept": 0, "RequiresCustomerAuthorization": false }"""

    def test_product(self):
        """Test creating product object"""
        from unfi_api.search.result import TopProduct
        result = Result.parse_obj(self.ordermanagement_files.brands_path_GetProductsByFullText_json)
        top_product = result.top_products[0]

        # result = TopProduct.parse_obj(self.ordermanagement_files.brands_path_GetProductsByFullText_json["TopProducts"][0])
        # product_listing = ProductListing.parse_obj(self.ordermanagement_files.brands_path_GetProductsByFullText_json[0])
        product_detail_int_id = ProductDetailIntId.parse_obj(
            self.ordermanagement_files.ProductDetail_GetProductDetailByProductIntId_json[0])
        product_data = ProductData.parse_obj(self.products_files.get_west_product_data_json)
        nutrition_facts = NutritionFacts.parse_obj({"nutrients": self.products_files.nutrition_json})
        # product_details = ProductDetail.parse_raw(self.product_details_json)
        attributes = Attributes.parse_obj(self.products_files.attributes_json)
        ingredients = Ingredients.parse_obj(self.products_files.ingredients_json)
        costs = Costs(self.ordermanagement_files.brands_GetProductDetailsFromService_xml)

        prodct_data_dict = {
            # "product_listing": product_listing,
            "product_data": product_data,
            "nutrition_facts": nutrition_facts,
            "attributes": attributes,
            "ingredients": ingredients,
            "product_details": product_detail_int_id,
            "costs": costs

        }
        combined_model_dicts = {}
        combined_model_dicts.update(product_data.dict())
        combined_model_dicts.update(product_detail_int_id.dict())
        # combined_model_dicts.update(nutrition_facts.dict())
        combined_model_dicts.update({attr: "Y" for attr in attributes.get_attribute_names()})
        combined_model_dicts.update(ingredients.dict())
        combined_model_dicts.update(costs.costs_to_dict())
        # combined_model_dicts.update(product_listing.dict())
        # print(combined_model_dicts)
        rows = [list(combined_model_dicts.keys())]
        rows.append([val for val in combined_model_dicts.values()])

        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        for row in rows:
            ws.append(row)

            wb.save("test.xlsx")

        # product_obj = product.UNFIProduct.parse_obj(prodct_data_dict)
        print(rows)
