from pydantic import Field
from typing import Optional

from pydantic.main import BaseModel


class Marketing(BaseModel):
    """
    BaseModel for marketing information from the UNFIApi
    """
    advertising_text: Optional[str] = Field(str, alias="Advertising Text")
    advertising_description: Optional[str] = Field(str, alias="Advertising Description")