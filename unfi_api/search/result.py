from __future__ import annotations
import concurrent.futures.thread
import re
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from typing import Any, Callable, Dict, List, Optional, Union, TYPE_CHECKING

from pydantic import BaseModel, Field, root_validator, validator
# from unfi_api.product import UNFIProduct
from unfi_api.utils.collections import normalize_dict
from unfi_api.utils.upc import stripcheckdigit

if TYPE_CHECKING:
    from unfi_api.product import UNFIProduct
    from unfi_api.client import UnfiApiClient

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

    def download(self, client:UnfiApiClient, callback: Callable = None) -> UNFIProduct:
        product = client.get_product(self)
        if callback:
            callback(product)
        return product


class Result(BaseModel):
    total_hits: Optional[int] = Field(None, alias="TotalHits")
    top_product_ids: Optional[List[int]] = Field(None, alias="TopProductIds")
    category_ids: Optional[List[int]] = Field(None, alias="CategoryIds")
    brand_ids: Optional[List[int]] = Field(None, alias="BrandIds")
    product_results: Optional[List[ProductResult]] = Field(None, alias="TopProducts")
    products: dict = {}

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
        self, client:UnfiApiClient, callback: Callable = None, threaded: bool=False, thread_count=10
    ) -> Dict[str, UNFIProduct]:
        """
        fetch products from api
        """
        if threaded:
            products = {}
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                try:
                    futures = [
                        executor.submit(
                            product.download, client
                        ) for product in self.product_results
                    ]
                    # done, not_done = wait(futures, timeout=0)
                    for future in as_completed(futures):
                        try:
                            product = future.result()
                            products[product.product_code] = product
                            callback(product)
                            if all([future.done() for future in futures]):
                                break
                        except Exception as e:
                            print(e)
                            raise
                        except KeyboardInterrupt:
                            executor.shutdown(wait=False)
                except KeyboardInterrupt:
                    executor._threads.clear()
                    concurrent.futures.thread._threads_queues.clear()
                    raise
           
        else:
            products = client.get_products(self, callback=callback)
        self.products.update(products)
        return products


class Results(BaseModel):

    __root__: Optional[List[Result]] = []

    @property
    def total_hits(self) -> int:
        return len(self.product_results)

    @property
    def top_product_ids(self) -> List[int]:
        ids = set()
        for result in self.__root__:
            ids.update(result.top_product_ids)
        return list(ids)

    @property
    def brand_ids(self) -> List[int]:
        ids = set()
        for result in self.__root__:
            ids.update(result.brand_ids)
        return list(ids)

    @property
    def category_ids(self) -> List[int]:
        ids = []
        for result in self.__root__:
            ids.extend(result.category_ids)
        return ids

    @property
    def product_results(self) -> List[ProductResult]:
        product_results = []
        result_ids = []
        for result in self.__root__:
            for product_result in result.product_results:
                if product_result.product_code not in result_ids:
                    product_results.append(product_result)
                    result_ids.append(product_result.product_code)
        return product_results

    def append_result(self, result: Result):
        self.__root__.append(result)

    def append_results(self, results: List[Result]):
        self.__root__.extend(results)

    def normalize(self):
        return normalize_dict(self.dict())

    def extend_results(self, results: Results):
        """append results from another results class. Ignorning duplicate product_codes"""
        for result in results.__root__:
            self.append_result(result)

    def download_products(
        self, client:UnfiApiClient, callback: Callable = None, threaded: bool=False
    ) -> Dict[str, Any]:
        """
        fetch products from api
        """
        products = client.get_products(self.product_results, callback=callback)
