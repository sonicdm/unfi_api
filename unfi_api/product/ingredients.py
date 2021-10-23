from datetime import date
from dateutil.parser import parse as date_parse
from pydantic import validator, Field
from pydantic.utils import to_camel
from typing import Optional

from pydantic.main import BaseModel

def snake_to_pascal_case(snake_str: str) -> str:
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)

class Ingredients(BaseModel):
    """
    base model representing ingredients from a unfi_api ingredients result
    {
  "Ingredients": "Annie's durum semolina pasta, original white Vermont cheddar cheese (milk, salt, cheese cultures, enzymes), whey, sweet cream buttermilk.",
  "ModifiedDate": "5/22/2020"
}
    """

    ingredients: str
    modified_date: date

    class Config:
        allow_population_by_field_name = True
        allow_population_by_alias = True
        fields = {
            "ingredients": "Ingredients",
            "modified_date": "ModifiedDate"
        }


    @validator("modified_date", pre=True)
    def parse_date_string(cls, v):
        if isinstance(v, str):
            return date_parse(v).date()
