from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator
from unfi_api.utils.collections import normalize_dict
from unfi_api.utils.upc import stripcheckdigit
# import unfi_api.product
if TYPE_CHECKING:
    from unfi_api.client import UnfiApiClient
    from unfi_api.product import UNFIProduct, UNFIProducts

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
    def root_validator(cls, values)-> dict:
        # print(values)
        upc = values.get("UPC")
        if upc is None:
            raise ValueError("upc is required")
        upc_no_check = stripcheckdigit(upc)
        values["upc_no_check"] = upc_no_check
        values["UPC"] = int(str(upc).replace("-", "").replace(" ", ""))

        for k, v in values.items():
            if isinstance(v, str):
                values[k] = v.title()
        return values

    def download(self, client:'UnfiApiClient', callback: Callable = None) -> UNFIProduct:
        product = client.get_product(self)
        if callback:
            callback(product)
        return product

    def __str__(self) -> str:
        return f"{self.product_code} - {self.brand_name} - {self.product_name} - {self.pack_size} - ({self.upc})"


class Result(BaseModel):
    # total_hits: Optional[int] = Field(0, alias="TotalHits")
    top_product_ids: Optional[List[int]] = Field(None, alias="TopProductIds")
    category_ids: Optional[List[int]] = Field(None, alias="CategoryIds")
    brand_ids: Optional[List[int]] = Field(None, alias="BrandIds")
    product_results: Optional[List[ProductResult]] = Field(None, alias="TopProducts")
    products: 'UNFIProducts' = None
    
    class Config:
        arbitrary_types_allowed = True
    
    @validator("products")
    def products_validator(v: Union[UNFIProducts, Dict[str, UNFIProduct]]) -> UNFIProducts:
        if isinstance(v, UNFIProducts):
            return v
        return UNFIProducts(**v)

    def normalize(self) -> dict:
        return normalize_dict(self.dict())

    def get_product_result_by_product_code(
        self, product_code: Union[str, int]
    ) -> Optional[ProductResult]:
        """
        product code must be int or str
        """
        product_code = str(product_code).zfill(5)
        for product in self.product_results:
            if product.product_code == product_code:
                return product
        return None

    def get_product_result_by_upc_ean13(
        self, upc: Union[str, int]
    ) -> Optional[ProductResult]:
        """
        product code must be int or str
        """
        upc = str(upc).zfill(13)
        for product in self.product_results:
            if product.upc == upc:
                return product
        return None

    def download_products(
        self, client:UnfiApiClient, callback: Callable = None, threaded: bool=False, thread_count=4
    ) -> 'UNFIProducts':
        """
        fetch products from api
        """
        products = client.get_products(self.product_results, callback=callback, threaded=threaded, thread_count=thread_count)
        if not self.products:
            self.products = products
        else:
            self.products.update(products)
        return products
    
    @property
    def total_hits(self) -> int:
        return len(self.product_results)
    
    
    def __len__(self) -> int:
        return len(self.product_results)
    
    def __str__(self) -> str:
        desc = f"Result: {self.total_hits} products"
        return desc


class Results(BaseModel):

    results: Optional[List[Result]] = Field([])
    product_results: Optional[List[ProductResult]] = Field([])

    
    @root_validator(pre=True)
    def root_validator(cls, values)-> dict:
        # print(values)
        # results: List[ProductResult] = values.get("results")
        # product_results = [res.dict(by_alias=True) for res in results]
        # cls.product_results.extend(product_results)
        # values['product_results'] = product_results
        return values
    @property
    def total_hits(self) -> int:
        return len(self.product_results)

    @property
    def top_product_ids(self) -> List[int]:
        ids = set()
        for result in self.results:
            ids.update(result.top_product_ids)
        return list(ids)

    @property
    def brand_ids(self) -> List[int]:
        ids = set()
        for result in self.results:
            ids.update(result.brand_ids)
        return list(ids)

    @property
    def category_ids(self) -> List[int]:
        ids = []
        for result in self.results:
            ids.extend(result.category_ids)
        return ids

    # @property
    # def product_results(self) -> List[ProductResult]:
    #     product_results = []
    #     result_ids = []
    #     for result in self.results:
    #         for product_result in result.product_results:
    #             if product_result.product_code not in result_ids:
    #                 product_results.append(product_result)
    #                 result_ids.append(product_result.product_code)
    #     return product_results

    def append_result(self, result: Result):
        for result in result.product_results:
            self.product_results.append(result)
        self.results.append(result)

    def append_results(self, results: List[Result]):
        for result in results:
            self.append_result(result)

    def normalize(self):
        return normalize_dict(self.dict())

    def extend_results(self, results: Results):
        """append results from another results class. Ignorning duplicate product_codes"""
        for result in results.results:
            self.append_result(result)

    def download_products(
        self, client:UnfiApiClient, callback: Callable = None, threaded: bool=False, thread_count=4, job_id: str = None
    ) -> UNFIProducts:
        """
        fetch products from api
        """
        products = client.get_products(self.product_results, callback=callback, threaded=threaded, thread_count=thread_count, job_id=job_id)
        return products

    def products(self):
        from unfi_api.product import UNFIProducts
        products = UNFIProducts()
        for result in self.results:
            for product in result.products:
                if result.products:
                    products.update(result.products)
        
    def __len__(self):
        return len(self.product_results)
    
    def clear(self):
        self.results = []
        self.product_results = []
    
    def remove_product_result(self, product_result: ProductResult):
        if product_result in self.product_results:
            self.product_results.remove(product_result)

def create_result(result_dict: dict=None) -> Result:
    result = Result(**result_dict)
    return result