import re
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator
from unfi_api.utils.collections import normalize_dict
from unfi_api.utils.upc import stripcheckdigit




class ProductResult(BaseModel):
    per_unit_price: Optional[float] = Field(..., alias="PerUnitPrice")
    is_sponsored: bool = Field(..., alias="IsSponsored")
    brand_id: int = Field(..., alias="BrandID")
    brand_name: str = Field(..., alias="BrandName")
    upc: int = Field(..., alias="UPC")
    upc_no_check: int
    product_code: str = Field(..., alias="ProductCode")
    product_name: str = Field(..., alias="ProductName")
    pack_size: str = Field(..., alias="PackSize")
    image_available: bool = Field(..., alias="ImageAvailable")
    total__rows: int = Field(..., alias="Total_Rows")
    price: float = Field(..., alias="Price")
    member_applicable_fee: float = Field(..., alias="MemberApplicableFee")
    discount: Any = Field(..., alias="Discount")
    product_int_id: int = Field(..., alias="ProductIntID")
    stock_avail: int = Field(..., alias="StockAvail")
    stock_oh: int = Field(..., alias="StockOH")
    units_in_full_case: int = Field(..., alias="UnitsInFullCase")
    minqty: int = Field(..., alias="MINQTY")
    category_id: int = Field(..., alias="CategoryID")
    plu: Any = Field(..., alias="PLU")
    search_rank: int = Field(..., alias="SearchRank")
    warehouse_message: Any = Field(..., alias="WarehouseMessage")
    is_new: bool = Field(..., alias="IsNew")

    @root_validator(pre=True)
    def root_validator(cls, values):
        # print(values)
        upc = values.get("UPC")
        if upc is None:
            raise ValueError("upc is required")
        upc_no_check = stripcheckdigit(upc)
        values["upc_no_check"] = upc_no_check
        values['UPC'] = int(str(upc).replace("-", "").replace(" ", ""))
        return values


class Result(BaseModel):
    total_hits: Optional[int] = Field(None, alias="TotalHits")
    top_product_ids: Optional[List[int]] = Field(None, alias="TopProductIds")
    category_ids: Optional[List[int]] = Field(None, alias="CategoryIds")
    brand_ids: Optional[List[int]] = Field(None, alias="BrandIds")
    products: Optional[List[ProductResult]] = Field(None, alias="TopProducts")

    def normalize(self):
        return normalize_dict(self.dict())

    def get_product_by_product_code(
        self, product_code: Union[str, int]
    ) -> Optional[ProductResult]:
        """
        product code must be int or str
        """
        product_code = str(product_code).zfill(5)
        for product in self.products:
            if product.product_code == product_code:
                return product
        return None

    def get_product_by_upc_ean13(self, upc: Union[str, int]) -> Optional[ProductResult]:
        """
        product code must be int or str
        """
        upc = str(upc).zfill(13)
        for product in self.products:
            if product.upc == upc:
                return product
        return None
