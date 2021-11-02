import re
from types import UnionType
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, root_validator, validator
from unfi_api.utils.collections import normalize_dict


def validate_ean13(ean13: Union[str, int]) -> bool:
    """
    Checks if a given EAN13 is valid using the check digit algorithm.
    example valid EAN-13: 9780521425575
    """
    # check if ean13 is a valid ean13

    ean13 = str(ean13).replace("-", "").replace(" ", "")
    try:
        ean13 = int(ean13)
    except ValueError:
        return False

    if len(ean13) <= 13:
        return False
    digits = [int(x) for x in ean13]
    check_digit = digits[-1]
    # sum all the digits in odd positions ignoring last place as check digit
    odd_sum = sum(digits[:-1][0::2])
    # sum all the digits in even positions
    even_sum = sum(digits[1::2])
    # multiply the result by 3
    even_sum *= 3
    # add the results of step 2 and step 3
    total = odd_sum + even_sum
    # take just the final digit (the ‘units’ digit) of the answer
    calculated_check_digit = total % 10
    if calculated_check_digit == check_digit:
        return True
    else:
        return False



def validate_upc(upc: str) -> bool:
    """
    :param upc: upc string
    :type upc: str
    :return: bool
    """
    # check if upc is exactly 12 digits
    upc = str(upc)
    if len(upc) <= 12:
        upc = upc.zfill(12)

    # validate CRC / check digit (sum of digits is a product of 10 after multiplying each odd digit by CRC)
    digits = list(map(int, upc))
    crc = digits[-1]
    total = sum([digit if i & 1 else digit * crc for i, digit in enumerate(digits)])
    return total % 10 == 0

def stripcheckdigit(upc: Union[int, str]) -> int:
    """
    :param upc: upc or ean13 string or int containing a check digit. Should remove the checkdigit and leave it alone if it
    has already had its check digit removed or is not a upc value.
    :type upc: str,int
    :param keep_formatting: keep the input formatting False by default
    :type keep_formatting: bool
    :return: int or str
    """
    # convert to string, replace dashes and spaces and pad to 12 places
    upc_str = str(upc).replace("-", "").replace(" ", "").zfill(12)
    try:
        int(upc_str)
    except ValueError:
        raise ValueError(f"upc: {upc:!r} must be a valid number or upc string.")
        
    # check if upc is a valid upc
    if len(upc_str) == 12 and validate_upc(upc_str):
        return int(upc_str[:-1])
    elif len(upc_str) == 13 and validate_ean13(upc_str):
        return int(upc_str[:-1])
    else:
        return int(upc_str)

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
