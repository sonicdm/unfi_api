from typing import Optional

from pydantic import BaseModel, Field, root_validator


class Marketing(BaseModel):
    """
    BaseModel for marketing information from the UNFIApi
    """
    advertising_text: Optional[str] = Field(..., alias="AdvertisingText")
    advertising_description: Optional[str] = Field(..., alias="AdvertisingDescription")

    @root_validator
    def check_advertising_text_and_description(cls, values):
        return values
