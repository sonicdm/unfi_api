from typing import Any, Optional
from pydantic import Field, BaseModel, validator


class LineItem(BaseModel):
    """
    Line item object to get placed in the invoice.
    """
    line_number: int = Field(..., alias='LN')
    ordered: int = Field(..., alias='Ord')
    shipped: int = Field(..., alias='Shp')
    pack_size: Optional[str] = Field(..., alias='Eaches - Pack')
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


    @validator('margin', pre=True)
    def validate_margin(cls, v):
        return float(int(v)/100)

    @property
    def case_size(self):
        size_split = self.pack_size.split("/")
        if len(size_split) > 1:
            return size_split[0]
        return
    
    @property
    def each_size(self):
        size_split = self.pack_size.split("/")
        if len(size_split) > 1:
            return "/".join(size_split[1:])
        return self.pack_size