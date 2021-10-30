from typing import Any, List, Optional
from pydantic import Field, BaseModel, validator, root_validator
from unfi_api.validators import currency_string_to_float


class LineItem(BaseModel):
    """
    Line item object to get placed in the invoice.
    """
    line_number: int = Field(..., alias='LN')
    ordered: int = Field(..., alias='Ord')
    shipped: int = Field(..., alias='Shp')
    pack_size: Optional[str] = Field(..., alias='Eaches - Pack')
    case_qty: Optional[int]
    each_size: Optional[str]
    pallet_name: Optional[str] = Field(..., alias='Pallet Name')
    upc: int = Field(..., alias='UPC')
    product_code: Optional[str] = Field(..., alias='Product Code')
    brand: Optional[str] = Field(..., alias='Brand')
    product_desc: Optional[str] = Field(..., alias='Product Desc')
    tax: Optional[str] = Field(..., alias='Tax')
    wholesale_case_price: float = Field(..., alias='Whls. Cs. T')
    wholesale_each_price: float = Field(..., alias='Whls. Ea.')
    reg_srp: float = Field(..., alias='Reg SRP')
    weight: float = Field(..., alias='Weight')
    ext_cube: Optional[float] = Field(..., alias='Ext. Cube')
    discount: Optional[Any] = Field(..., alias='Discount')
    net_case_price: float = Field(..., alias='Net - Case')
    net_each_price: float = Field(..., alias='Net - Each')
    net_srp: float = Field(..., alias='SRP')
    margin: float = Field(..., alias='Margin')
    ext_price: float = Field(..., alias='Ext. Price')
    disc_reas: str = Field(..., alias='Disc. Reas')


    # validators
    # currency to float
    _currency_to_float = validator('wholesale_case_price', 'wholesale_each_price', 'reg_srp', 'net_case_price',
                                   'net_each_price', 'net_srp', 'margin', 'ext_price', always=True,
                                   pre=True, allow_reuse=True)(currency_string_to_float)

    @root_validator(pre=True)
    def split_pack_size(cls, values: dict) -> dict:
        """
        Splits the pack size into a case_qty and each_size.
        """
        pack_size = values.get('Eaches - Pack', values.get('pack_size'))
        if pack_size:
            size_split = pack_size.split("/")
            if len(size_split) > 1:
                case_qty = int(size_split[0])
                each_size = "/".join(size_split[1:])
            else:
                case_qty = 1
                each_size = size_split[0]
            values['case_qty'] = case_qty
            values['each_size'] = each_size
        return values

    @validator("upc")
    def _upc_validator(cls, value: str) -> int:
        """
        Validator for UPC.
        """
        value = int(value)
        if value < 0:
            raise ValueError("UPC must be a positive integer.")
        return value

    @validator('margin', pre=True)
    def validate_margin(cls, v):
        return float(int(v) / 100)

    # Properties
    # @property
    # def case_size(self):
    #     size_split = self.pack_size.split("/")
    #     if len(size_split) > 1:
    #         return size_split[0]
    #     return

    # @property
    # def each_size(self):
    #     size_split = self.pack_size.split("/")

    #     return sel    #     if len(size_split) > 1:
    #     #         return "/".join(size_split[1:])f.pack_size


class LineItems(BaseModel):
    """
    Line item object to get placed in the invoice.
    """
    __root__: List[LineItem] = []

    # @classmethod
    @root_validator(pre=True)
    def validate_line_items(cls, values: dict):
        print(values)
        if not isinstance(values['__root__'], list):
            raise ValueError('LineItems must be a list')
        new_list = []
        for line_item in values['__root__']:
            if line_item[
                'Ord'] == '':  # we never want a line item with no ordered amount as it has worthless information for these purposes
                continue
            new_list.append(line_item)
        values['__root__'] = new_list
        return values

    @property
    def line_items(self):
        return self.__root__
