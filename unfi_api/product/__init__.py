from datetime import date, datetime
from typing import Any, Dict, Optional
from dateutil.parser import parse as date_parse
from pydantic import BaseModel, Field, validator
from pydantic.class_validators import root_validator

from unfi_api.product.attributes import Attributes
from unfi_api.product.marketing import Marketing
from unfi_api.product.ingredients import Ingredients
from unfi_api.product.nutrition import NutritionFacts
from unfi_api.product.pricing import Pricing
from unfi_api.search.result import ProductResult
from unfi_api.utils.collections import flatten_dict_overwrite, normalize_dict


class ProductData(BaseModel):
    """
    BaseModel for product details from the UNFIApi getwestproductdata endpoint
    """

    product_id: str = Field(..., alias="productID")
    effective_date: date = Field(..., alias="effectiveDate")
    status: str
    net_price: float = Field(..., alias="netPrice")
    retail_price: float = Field(..., alias="retailPrice")
    price_reason: str = Field(..., alias="priceReason")
    margin: float
    stock_oh: int = Field(..., alias="stockOh")
    stock_avail: int = Field(..., alias="stockAvail")
    allow: str
    refers_to: str = Field(..., alias="refersTo")
    buyer_notes: str = Field(..., alias="buyerNotes")
    buyer_code: str = Field(..., alias="buyerCode")

    @validator("effective_date", pre=True, allow_reuse=True)
    def validate_effective_date(cls, v):
        """convert string to date"""
        return date_parse(v)

    @validator("net_price", "retail_price", pre=True)
    def validate_price(cls, v):
        """remove currency symbol from price and convert to float"""
        return float(str(v).replace("$", ""))

    @validator("margin", pre=True)
    def validate_margin(cls, v):
        """remove percent symbol and convert text representation of percent to actual percent"""
        margin = v.replace("%", "")
        margin = float(margin)
        return margin / 100


class ProductDetailIntId(BaseModel):
    """
    BaseModel for product details from the UNFIApi product detail by intid
    """

    stock_avail: int = Field(..., alias="StockAvail")
    stock_oh: int = Field(..., alias="StockOH")
    per_unit_price: float = Field(..., alias="PerUnitPrice")
    brand_id: int = Field(..., alias="BrandId")
    brand_name: str = Field(..., alias="BrandName")
    product_int_id: int = Field(..., alias="ProductIntID")
    product_code: str = Field(..., alias="ProductCode")
    product_name: str = Field(..., alias="ProductName")
    discount: str = Field(..., alias="Discount")
    upc: int = Field(..., alias="UPC")
    pack_size: str = Field(..., alias="PackSize")
    price: float = Field(..., alias="Price")
    units_in_full_case: int = Field(..., alias="UnitsInFullCase")
    minqty: int = Field(..., alias="MINQTY")
    inner_case_upc: int = Field(..., alias="InnerCaseUPC")
    master_case_upc: int = Field(..., alias="MasterCaseUPC")
    plu: Any = Field(..., alias="PLU")
    pv_label_code: str = Field(..., alias="PVLabelCode")
    member_applicable_fee: float = Field(..., alias="MemberApplicableFee")
    organic_code: str = Field(..., alias="OrganicCode")
    sub_header: str = Field(..., alias="SubHeader")
    category_id: int = Field(..., alias="CategoryID")
    category_name: str = Field(..., alias="CategoryName")
    country_of_origin_id: int = Field(..., alias="CountryOfOriginID")
    country_of_origin_name: str = Field(..., alias="CountryOfOriginName")
    warehouse_message: Any = Field(..., alias="WarehouseMessage")
    is_new: bool = Field(..., alias="IsNew")

    @validator("upc", "inner_case_upc", "master_case_upc", pre=True)
    def validate_upc(cls, v):
        return int(v.replace("-", ""))
    



class ProductListing(BaseModel):
    product_int_id: int = Field(..., alias="ProductIntID")
    division_code: str = Field(..., alias="DivisionCode")
    product_number: str = Field(..., alias="ProductNumber")
    product_name: str = Field(..., alias="ProductName")
    category_id: int = Field(..., alias="CategoryID")
    brand_id: int = Field(..., alias="BrandID")
    sub_header_id: int = Field(..., alias="SubHeaderID")
    department_id: int = Field(..., alias="DepartmentID")
    upc: float = Field(..., alias="UPC")
    inner_case_upc: float = Field(..., alias="InnerCaseUPC")
    master_case_upc: float = Field(..., alias="MasterCaseUPC")
    plu: Any = Field(..., alias="PLU")
    organic_code: str = Field(..., alias="OrganicCode")
    speciality_flag: str = Field(..., alias="SpecialityFlag")
    country_of_origin_id: int = Field(..., alias="CountryOfOriginID")
    is_private_label: str = Field(..., alias="IsPrivateLabel")
    product_owner: str = Field(..., alias="ProductOwner")
    ingredients: str = Field(..., alias="Ingredients")
    img_file_name: str = Field(..., alias="ImgFileName")
    img_url: Optional[str] = Field(..., alias="ImgUrl")
    is_image_available: bool = Field(..., alias="IsImageAvailable")
    minimum_order_quantity: int = Field(..., alias="MinimumOrderQuantity")
    substitute_number: Optional[str] = Field(..., alias="SubstituteNumber")
    short_description: str = Field(..., alias="ShortDescription")
    long_description: Optional[str] = Field(..., alias="LongDescription")
    search_keywords: Any = Field(..., alias="SearchKeywords")
    pack_size: str = Field(..., alias="PackSize")
    units_in_full_case: int = Field(..., alias="UnitsInFullCase")
    unit_type: Any = Field(..., alias="UnitType")
    size: Any = Field(..., alias="Size")
    created_by: int = Field(..., alias="CreatedBy")
    created_date: datetime = Field(..., alias="CreatedDate")
    modified_by: int = Field(..., alias="ModifiedBy")
    modified_date: datetime = Field(..., alias="ModifiedDate")
    is_active: bool = Field(..., alias="IsActive")
    is_deleted: bool = Field(..., alias="IsDeleted")
    private_lbl_dept: int = Field(..., alias="PrivateLblDept")
    requires_customer_authorization: bool = Field(
        ..., alias="RequiresCustomerAuthorization"
    )

    @validator("upc", "inner_case_upc", "master_case_upc", pre=True)
    def validate_upc(cls, v):
        return int(v.replace("-", ""))

    @validator("created_date", "modified_date", pre=True)
    def validate_date(cls, v):
        return date_parse(v)


"""
# class that combines
# Attributes
# Marketing
# Ingredients
# NutritionFacts
# Costs
"""


class UNFIProduct(BaseModel):
    data_by_int_id: ProductDetailIntId
    data: ProductData
    attributes: Optional[Attributes]
    marketing: Optional[Marketing]
    ingredients: Optional[Ingredients]
    nutrition_facts: Optional[NutritionFacts]
    pricing: Pricing
    listing: ProductResult

    class Config:
        arbitrary_types_allowed = True

    def normalize(self, **kwargs) -> dict:
        """pass to base model dict method"""
        return normalize_dict(self.dict(**kwargs))

    def flatten(self, **kwargs) -> dict:
        """pass to base model dict method"""
        return flatten_dict_overwrite(self.dict(**kwargs))


# class UNFIProduct(BaseModel):
#     """
#     class containing all the product data from a unfi_api search result.
#     attributes, nutrition, productdata, productdetails, ingredients, marketingm pricing
#     """

#     attributes: Optional[Attributes]
#     nutrition: Optional[NutritionFacts]
#     productdata: Optional[ProductData]
#     productdetails: Optional[ProductDetailIntId]
#     ingredients: Optional[Ingredients]
#     marketing: Optional[Marketing]
#     costs: Optional[Costs]

#     # nutrition: NutritionFacts
#     # productdata: ProductData
#     # productdetails: ProductDetailIntId
#     # product_listing: ProductListing
#     # ingredients: Ingredients
#     # marketing: Marketing
#     combined_product_details: Dict[str, Any] = {}

#     # get promo cost
#     def get_promo_cost_records(self):
#         costs = []
#         for cost in self.pricing:
#             if cost.price_type is not "R":
#                 costs.append(cost)
#         return costs

#     # get retail cost
#     def retail_cost_record(self):
#         for cost in self.pricing:
#             if cost.price_type is "R":
#                 return cost

#     # retrieve the dict from each object and return as a combined dict of all values combined
#     def get_combined_data(self):
#         if not self.combined_product_details:
#             self.combined_product_details = {**self.attributes.get_values(), **self.nutrition.get_values(), **self.productdata.get_values(
#             ), **self.productdetails.get_values(), **self.ingredients.get_values(), **self.marketing.get_values()}
#         return self.combined_product_details

#     @property
#     def wholesale_case_price(self):
#         return self.retail_cost_record().case_price

#     @property
#     def wholesale_unit_price(self):
#         return self.retail_cost_record().unit_price

#     @property
#     def srp(self):
#         return self.retail_cost_record().retail_price

#     # current price of the product from product data net price
#     @property
#     def current_price(self):
#         return self.productdata.net_price

#     # price_reason of the product from product data price reason
#     @property
#     def price_reason(self):
#         return self.productdata.price_reason

#     # product code
#     @property
#     def product_code(self):
#         return self.productdata.product_id

#     # product name
#     @property
#     def product_name(self):
#         return self.productdetails.product_name

#     # title case brand name
#     @property
#     def brand_name(self):
#         return self.attributes.brand_name.title()

#     # stock on hand
#     @property
#     def stock_oh(self):
#         return self.productdata.stock_oh

#     # stock available
#     @property
#     def stock_avail(self):
#         return self.productdata.stock_avail

#     # product id
#     @property
#     def product_id(self):
#         return self.productdata.product_id

#     # short description
#     @property
#     def short_description(self):
#         return self.productdetails.short_description

#     # long description
#     @property
#     def long_description(self):
#         return self.productdetails.long_description

#     # size with units in full case removed so 12/12/16 oz is 12/16 oz
#     @property
#     def size(self):
#         # if no split return whole value
#         if len(self.productdata.pack_size.split("/")) == 1:
#             return self.productdata.pack_size
#         else:
#             return "/".join(self.productdata.size.split("/")[1:])


r"""
class Product(object):

    def __init__(
            self, product=None, product_data=None, product_detail=None, marketing=None, ingredients=None,
            nutrition_facts=None,
            attributes=None, pricing=None
    ):
        # Identifiers
        self.product_code = None
        self.product_int_id = None
        self.product_number = None
        self.upc = None
        self.master_case_upc = None
        self.inner_case_upc = None
        self.plu = None
        self.substitute_number = None

        # Descriptions
        self.department_id = None
        self.brand_id = None
        self.brand_name = None
        self.category_id = None
        self.category_name = None
        self.product_name = None
        self.short_description = None
        self.long_description = None
        self.sub_header = None
        self.sub_header_id = None
        self.size = None
        self.pack_size = None
        self.unit_type = None
        self.units_in_full_case = None
        self.speciality_flag = None
        self.organic_code = None
        self.country_of_origin_id = None
        self.country_of_origin_name = None

        # Pricing & Availability
        # self.stock_avail = None
        # self.stock_oh = None
        self.discount = None
        self.per_unit_price = None
        self.price = None
        self.minimum_order_quantity = None
        self.minqty = None

        # Image Info
        self.image_available = None
        self.img_file_name = None
        self.img_url = None
        self.is_image_available = None

        # Unused
        self.search_keywords = None
        self.is_new = None
        self.is_private_label = None
        self.is_sponsored = None
        self.private_lbl_dept = None
        self.product_owner = None
        self.pvlabel_code = None
        self.total_rows = None
        self.warehouse_message = None
        self.created_by = None
        self.created_date = None
        self.modified_by = None
        self.modified_date = None
        self.is_active = None
        self.is_deleted = None
        self.requires_customer_authorization = None
        self.member_applicable_fee = None
        self.division_code = None

        # Objects
        self._attributes = []
        self.marketing = None
        self.ingredients = None
        self.nutrition_facts = None
        self._pricing = None

        # Protected Attributes
        self.__stock_avail = None
        self.__stock_oh = None
        self.__upc = None
        self.__master_case_upc = None
        self.__inner_case_upc = None

        if product:
            self.from_dict(product)
        if product_data:
            self.from_dict(product_data)
        if product_detail:
            self.from_dict(product_detail)
        if attributes:
            for attribute in attributes:
                self._attributes.append(Attribute(**attribute))
        if ingredients:
            self.ingredients = Ingredients(**ingredients)
        if marketing:
            self.marketing = Marketing(**marketing)
        if nutrition_facts:
            self.nutrition_facts = NutritionFacts(nutrition_facts)
        if pricing:
            self._pricing = Pricing(pricing)

        pass

    def from_dict(self, d):
        for k, v in d.items():
            setattr(self, camel_to_snake_case(k), strings_to_numbers(v))
            # print("self.%s = None" % camel_to_snake_case(k))

    @property
    def stock_oh(self):
        return self.__stock_oh

    @stock_oh.setter
    def stock_oh(self, value):
        if self.__stock_oh:
            if abs(self.__stock_oh) < abs(value):
                self.__stock_oh = value
        else:
            self.__stock_oh = value

    @property
    def stock_avail(self):
        return self.__stock_avail

    @stock_avail.setter
    def stock_avail(self, value):
        if self.__stock_avail:
            if abs(self.__stock_avail) < abs(value):
                self.__stock_avail = value
        else:
            self.__stock_avail = value

    @property
    def upc(self):
        return self.__upc

    @upc.setter
    def upc(self, value):
        if value:
            if isinstance(value, str):
                value = re.sub(r"\W", "", value)
            self.__upc = int(value)

    @property
    def master_case_upc(self):
        return self.__master_case_upc

    @master_case_upc.setter
    def master_case_upc(self, value):
        if value:
            self.__master_case_upc = int(value)

    @property
    def inner_case_upc(self):
        return self.__inner_case_upc

    @inner_case_upc.setter
    def inner_case_upc(self, value):
        if value:
            self.__inner_case_upc = int(value)

    @property
    def pricing(self):
        return list(self._pricing)

    def update(self, d):
        self.from_dict(d)

    def get_values(self):
        out = {}
        for k, v in inspect.getmembers(self):
            if not str(k).startswith("_") and not callable(v):
                out[k] = v
        return out

    def __repr__(self):

        items = {
            "brand": self.brand_name,
            "long_description": self.long_description,
            "short_description": self.short_description,
            "size": self.size,
            "pack_size": self.pack_size,
        }

        items = ("%s = %r" % (k, v) for k, v in self.get_values().items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))
"""
