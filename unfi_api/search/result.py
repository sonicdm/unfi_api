from pydantic import BaseModel, Field, validator, root_validator
from typing import Any, Optional, List
from unfi_api.utils import normalize_dict


class ProductResult(BaseModel):
    per_unit_price: Optional[float] = Field(..., alias='PerUnitPrice')
    is_sponsored: bool = Field(..., alias='IsSponsored')
    brand_id: int = Field(..., alias='BrandID')
    brand_name: str = Field(..., alias='BrandName')
    upc: str = Field(..., alias='UPC')
    product_code: str = Field(..., alias='ProductCode')
    product_name: str = Field(..., alias='ProductName')
    pack_size: str = Field(..., alias='PackSize')
    image_available: bool = Field(..., alias='ImageAvailable')
    total__rows: int = Field(..., alias='Total_Rows')
    price: float = Field(..., alias='Price')
    member_applicable_fee: float = Field(..., alias='MemberApplicableFee')
    discount: Any = Field(..., alias='Discount')
    product_int_id: int = Field(..., alias='ProductIntID')
    stock_avail: int = Field(..., alias='StockAvail')
    stock_oh: int = Field(..., alias='StockOH')
    units_in_full_case: int = Field(..., alias='UnitsInFullCase')
    minqty: int = Field(..., alias='MINQTY')
    category_id: int = Field(..., alias='CategoryID')
    plu: Any = Field(..., alias='PLU')
    search_rank: int = Field(..., alias='SearchRank')
    warehouse_message: Any = Field(..., alias='WarehouseMessage')
    is_new: bool = Field(..., alias='IsNew')

    @root_validator(pre=True)
    def root_validator(cls, values):
        print(values)
        return values


class Result(BaseModel):
    total_hits: Optional[int] = Field(None, alias='TotalHits')
    top_product_ids: Optional[List[int]] = Field(None, alias='TopProductIds')
    category_ids: Optional[List[int]] = Field(None, alias='CategoryIds')
    brand_ids: Optional[List[int]] = Field(None, alias='BrandIds')
    products: Optional[List[ProductResult]] = Field(None, alias='TopProducts')

    def normalize(self):
        return normalize_dict(self.dict())
