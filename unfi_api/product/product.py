from __future__ import annotations
from datetime import date, datetime
import re
from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Optional, Tuple, Union

from dateutil.parser import parse as date_parse
from pydantic import BaseModel, Field, validator
from pydantic.class_validators import root_validator
from unfi_api.product.attributes import Attributes
from unfi_api.product.ingredients import Ingredients
from unfi_api.product.marketing import Marketing
from unfi_api.product.nutrition import NutritionFacts
from unfi_api.product.pricing import Cost, Pricing
from unfi_api.utils.collections import flatten_dict_overwrite, lower_case_keys, normalize_dict
from unfi_api.utils.upc import stripcheckdigit
from unfi_api.utils.string import clean_size_field
from unfi_api.search.result import ProductResult
if TYPE_CHECKING:
    from unfi_api import UnfiApiClient

class ProductIntID(BaseModel):
    product_int_id: int = Field(..., alias='ProductIntID')
    division_code: str = Field(..., alias='DivisionCode')
    product_code: str = Field(..., alias='ProductNumber')
    product_name: str = Field(..., alias='ProductName')
    category_id: int = Field(..., alias='CategoryID')
    brand_id: int = Field(..., alias='BrandID')
    sub_header_id: Any = Field(..., alias='SubHeaderID')
    department_id: int = Field(..., alias='DepartmentID')
    upc: str = Field(..., alias='UPC')
    inner_case_upc: str = Field(..., alias='InnerCaseUPC')
    master_case_upc: str = Field(..., alias='MasterCaseUPC')
    plu: Any = Field(..., alias='PLU')
    organic_code: str = Field(..., alias='OrganicCode')
    speciality_flag: str = Field(..., alias='SpecialityFlag')
    country_of_origin_id: Optional[int] = Field(..., alias='CountryOfOriginID')
    is_private_label: str = Field(..., alias='IsPrivateLabel')
    product_owner: str = Field(..., alias='ProductOwner')
    ingredients: Optional[str] = Field(..., alias='Ingredients')
    img_file_name: Optional[str] = Field(..., alias='ImgFileName')
    img_url: Any = Field(..., alias='ImgUrl')
    is_image_available: bool = Field(..., alias='IsImageAvailable')
    minimum_order_quantity: int = Field(..., alias='MinimumOrderQuantity')
    substitute_number: Any = Field(..., alias='SubstituteNumber')
    short_description: Optional[str] = Field(..., alias='ShortDescription')
    long_description: Any = Field(..., alias='LongDescription')
    search_keywords: Any = Field(..., alias='SearchKeywords')
    pack_size: str = Field(..., alias='PackSize')
    units_in_full_case: int = Field(..., alias='UnitsInFullCase')
    unit_type: Any = Field(..., alias='UnitType')
    size: Any = Field(..., alias='Size')
    created_by: int = Field(..., alias='CreatedBy')
    created_date: str = Field(..., alias='CreatedDate')
    modified_by: int = Field(..., alias='ModifiedBy')
    modified_date: str = Field(..., alias='ModifiedDate')
    is_active: bool = Field(..., alias='IsActive')
    is_deleted: bool = Field(..., alias='IsDeleted')
    private_lbl_dept: int = Field(..., alias='PrivateLblDept')
    requires_customer_authorization: bool = Field(
        ..., alias='RequiresCustomerAuthorization'
    )

    @validator('is_image_available', pre=True)
    def is_image_available_validator(cls, v):
        return True if v else False


class ProductData(BaseModel):
    """
    BaseModel for product details from the UNFIApi getwestproductdata endpoint
    """

    product_code: str = Field(..., alias="productID")
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

    brand_name: str = Field(..., alias="BrandName")
    product_name: str = Field(..., alias="ProductName")
    sub_header: str = Field(..., alias="SubHeader")
    # short_description: Optional[str] = Field(..., alias="ShortDescription")
    organic_code: str = Field(..., alias="OrganicCode")
    units_in_full_case: int = Field(..., alias="UnitsInFullCase")
    pack_size: str = Field(..., alias="PackSize")
    upc: int = Field(..., alias="UPC")
    stock_avail: int = Field(..., alias="StockAvail")
    stock_oh: int = Field(..., alias="StockOH")
    per_unit_price: float = Field(..., alias="PerUnitPrice")
    brand_id: int = Field(..., alias="BrandId")
    product_int_id: int = Field(..., alias="ProductIntID")
    product_code: Optional[str] = Field(..., alias="ProductCode")
    discount: Optional[str] = Field(..., alias="Discount")
    price: float = Field(..., alias="Price")
    minqty: int = Field(..., alias="MINQTY")
    inner_case_upc: int = Field(..., alias="InnerCaseUPC")
    master_case_upc: int = Field(..., alias="MasterCaseUPC")
    plu: Any = Field(..., alias="PLU")
    pv_label_code: str = Field(..., alias="PVLabelCode")
    member_applicable_fee: float = Field(..., alias="MemberApplicableFee")
    category_id: int = Field(..., alias="CategoryID")
    category_name: str = Field(..., alias="CategoryName")
    country_of_origin_id: Optional[int] = Field(..., alias="CountryOfOriginID")
    country_of_origin_name: Optional[str] = Field(..., alias="CountryOfOriginName")
    warehouse_message: Any = Field(..., alias="WarehouseMessage")
    is_new: bool = Field(..., alias="IsNew")

    @root_validator(pre=True)
    def field_values_to_title_case(cls, values):
        """convert all field values to title case"""
        # for k,v in values.items():
        #     if k not in ['pack_size', 'category_name','PackSize', "CategoryName", "OrganicCode","organic_code"]:
        #         if isinstance(v, str):
        #             values[k] = v.title()
        return values

    @validator("upc", "inner_case_upc", "master_case_upc", pre=True)
    def validate_upc(cls, v):
        return int(v.replace("-", ""))

    @property
    def case_qty(self):
        return self.units_in_full_case

    @property
    def unit_size(self):
        return clean_size_field(self.pack_size)
    



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
    
    # ID's
    upc: int
    upc_no_check: int
    master_case_upc: int
    inner_case_upc: int
    product_int_id: int
    product_code: str

    # descriptions
    brand: str
    description: str
    short_description: Optional[str]
    long_description: Optional[str]
    category: str
    organic_code: str
    image_url: str
    image_available: bool


    # retail pricing
    case_price: float
    unit_price: float
    retail_margin: float
    retail_price: float

    # case info
    case_qty: int
    unit_size: str

    # sub models
    data_by_int_id: ProductDetailIntId
    int_id: ProductIntID
    data: ProductData
    attributes: Optional[Attributes]
    marketing: Optional[Marketing]
    ingredients: Optional[Ingredients]
    nutrition_facts: Optional[NutritionFacts]
    pricing: Pricing
    listing: ProductResult
    

    class Config:
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def root_validator(cls, values: dict):
        data_by_int_id: ProductDetailIntId = values.get("data_by_int_id")
        pricing: Pricing = values.get("pricing")
        product_data: ProductData = values.get("data")
        int_id: ProductIntID = values.get("int_id")

        supplemental_data_dict: dict = {}

        # get product ids
        product_int_id: int = data_by_int_id.product_int_id
        product_code: str = data_by_int_id.product_code
        upc = data_by_int_id.upc
        upc_no_check = stripcheckdigit(upc)
        master_case_upc = data_by_int_id.master_case_upc
        inner_case_upc = data_by_int_id.inner_case_upc
        ######
        supplemental_data_dict["product_int_id"] = product_int_id
        supplemental_data_dict["product_code"] = product_code
        supplemental_data_dict["upc"] = upc
        supplemental_data_dict["upc_no_check"] = upc_no_check
        supplemental_data_dict["master_case_upc"] = master_case_upc
        supplemental_data_dict["inner_case_upc"] = inner_case_upc

        # get description info
        description = data_by_int_id.product_name.replace("`", "'").replace("'S","'s")
        description = re.sub(r"( At Least \d+% Organic| 100% Organic)", "", description)
        brand = data_by_int_id.brand_name.title().replace("`", "'").replace("'S","'s")
        short_description = int_id.short_description
        long_description = int_id.long_description
        category = data_by_int_id.category_name
        organic_code = data_by_int_id.organic_code
        image_available = int_id.is_image_available
        image_url = "https://products.unfi.com/api/Images/"+str(product_int_id)
        ######
        supplemental_data_dict["description"] = description
        supplemental_data_dict["brand"] = brand
        supplemental_data_dict["short_description"] = short_description
        supplemental_data_dict["long_description"] = long_description
        supplemental_data_dict["category"] = category
        supplemental_data_dict["organic_code"] = organic_code
        supplemental_data_dict["image_available"] = image_available
        supplemental_data_dict["image_url"] = image_url

        # get pricing info from Pricing
        case_price = pricing.case_price
        unit_price = pricing.unit_price
        retail_margin = pricing.retail_margin
        retail_price = pricing.retail_price
        ######
        supplemental_data_dict["case_price"] = case_price
        supplemental_data_dict["unit_price"] = unit_price
        supplemental_data_dict["retail_margin"] = retail_margin
        supplemental_data_dict["retail_price"] = retail_price

        # get case info from product_detail_int_id
        pack_size = data_by_int_id.pack_size
        case_qty = data_by_int_id.units_in_full_case
        unit_size = clean_size_field(pack_size)
        ######
        supplemental_data_dict["pack_size"] = pack_size
        supplemental_data_dict["case_qty"] = case_qty
        supplemental_data_dict["unit_size"] = unit_size

        # get stock info from product_data
        stock_oh = product_data.stock_oh
        stock_avail = product_data.stock_avail
        ######
        supplemental_data_dict["stock_oh"] = stock_oh
        supplemental_data_dict["stock_avail"] = stock_avail

        values.update(supplemental_data_dict)
        return values
        
    def normalize(self, **kwargs) -> dict:
        """pass to base model dict method"""
        return normalize_dict(self.dict(**kwargs))

    def flatten(self, **kwargs) -> dict:
        """pass to base model dict method"""
        return flatten_dict_overwrite(self.dict(**kwargs))

    
    def to_excel(self, exclude=None, include=None) -> dict:
        """pass to base model dict method"""
        if not exclude:
            exclude = {"pricing", "ingredients", "nutrition_facts", "attributes"}
        attributes = self.attributes.get_attribute_flags()
        prices = self.pricing.costs_to_dict()
        out_dict = self.dict(exclude=exclude, include=include)
        out_dict.update(attributes)
        out_dict.update(prices)
        out_dict = lower_case_keys(out_dict)
        return flatten_dict_overwrite(out_dict)
    
    def get_image(self, client: 'UnfiApiClient'):
        if self.image_available:
            return client.get_product_image(self.int_id)
        else:
            return None
            



class UNFIProducts:
    
    def __init__(self, products: Dict[str, UNFIProduct]={}) -> None:
        if isinstance(products, UNFIProducts):
            products = products.products_dict
        self.products_dict = products
        
    def to_excel(self, exclude=None, include=None) -> List[dict]:
        """
        pass to base model to_excel method
        exclude and include are fields to exclude and include from the UnfiProduct model dict
        """

        products = {product.product_code: product.to_excel(exclude=exclude, include=include) for product in self.products_dict.values()}
        return products
    
    def product_codes(self) -> List[str]:
        """generator of product codes"""
        for code in self.products_dict.keys():
            yield code

    def products(self) -> List[UNFIProduct]:
        """generator of products"""
        for product in self.products_dict.values():
            yield product
            
    def __iter__(self) -> Iterator[UNFIProduct]:
        """pass to base model __iter__ method"""
        return self.products()
    
    def __getitem__(self, key: str) -> UNFIProduct:
        """pass to base model __getitem__ method"""
        return self.products_dict[key]
    
    def __len__(self) -> int:
        """pass to base model __len__ method"""
        return len(self.products_dict)
    
    def __repr__(self) -> str:
        """pass to base model __repr__ method"""
        return f"<UNFIProducts: {len(self.products_dict)} products>"
    
    def update(self, products: Union[Dict[str, UNFIProduct], UNFIProducts]) -> None:
        """pass to base model update method"""
        if isinstance(products, UNFIProducts):
            self.products_dict.update(products.products_dict)
        elif isinstance(products, dict):
            self.products_dict.update(products)
        else:
            raise TypeError(f"products must be a dict or UNFIProducts, not {type(products)}")
