from datetime import date
from dateutil.parser import parse as date_parse
from typing import Any, Iterator, Optional, List, Dict
from pydantic import Field, BaseModel, validator
from pydantic.class_validators import root_validator
from pydantic.utils import to_camel
import re


def snake_to_pascal_case(snake_str: str) -> str:
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)


def pascal_to_snake_case(pascal_str: str) -> str:
    components = re.findall(r'[A-Z][^A-Z]{2,}?', pascal_str)
    return '_'.join(components).lower()


def string_to_bool(string: str) -> bool:
    """
    any value in y,1,true, yes, t will return True
    any value in n,0,false, no, f will return False
    """
    string = str(string)
    if string.lower() in ('y', 'yes', 'true', 't', '1'):
        return True
    elif string.lower() in ('n', 'no', 'false', 'f', '0'):
        return False
    else:
        raise ValueError(f'{string} is not a valid boolean')


class Attribute(BaseModel):
    """
    BaseModel for attributes from the UNFIApi
    {'AttributeID': 22, 'AttributeName': 'Kosher', 'SourceOfAttributeData': 'PWS', 'CreatedBy': 10, 'CreatedDate': '2015-09-05T02:01:08.597', 'ModifiedBy': 10, 'ModifiedDate': '2015-09-05T02:01:08.597', 'Active': '1'}
    """
    attribute_id: int = Field(int, description="The unique identifier for the attribute", alias="AttributeID")
    attribute_name: str = Field(str, description="The name of the attribute", alias="AttributeName")
    source_of_attribute_data: str = Field(str, description="The source of the attribute data",
                                          alias="SourceOfAttributeData")
    created_by: int = Field(int, description="The user id of the user who created the attribute", alias="CreatedBy")
    created_date: Any = Field(date, description="The date the attribute was created", alias="CreatedDate")
    modified_by: int = Field(int, description="The user id of the user who modified the attribute", alias="ModifiedBy")
    modified_date: Any = Field(date, description="The date the attribute was modified", alias="ModifiedDate")
    active: bool = Field(str, description="The active status of the attribute", alias="Active")

    @validator("created_date", "modified_date", allow_reuse=True)
    def string_to_date(cls, v) -> date:
        return date_parse(v).date()

    @validator("active", allow_reuse=True)
    def string_to_bool(cls, v) -> bool:
        return string_to_bool(v)


class Attributes(BaseModel):
    """
    BaseModel for attributes from the UNFIApi
    """
    __root__: List[Attribute] = []

    # def __init__(self, attributes: Optional[dict] = None):
    #     self.attributes: List[Attribute] = []
    #     if attributes:
    #         for attribute in attributes:
    #             self.add_attribute(attribute)

    # root_validator("attributes", allow_reuse=True, pre=True)
    # def attribute_validator(self, v) -> List[Attribute]:
    #     if not isinstance(v, list):
    #         raise ValueError(f'{v} is not a list')
    #     for attribute in v:
    #         if not isinstance(attribute, dict):
    #             raise ValueError(f'{attribute} is not a dict')
    #     return v
            
    @property
    def attributes(self) -> List[Attribute]:
        """
        Get the attributes
        """
        return self.__root__

    def add_attribute(self, attribute: dict) -> None:
        """
        Add an attribute to the list of attributes
        """
        self.attributes.append(Attribute(**attribute))

    def get_attribute(self, attribute_id: int) -> Optional[Attribute]:
        """
        Get an attribute by its ID
        """
        for attribute in self.attributes:
            if attribute.attribute_id == attribute_id:
                return attribute
        return None

    def get_attributes(self, attribute_name: str) -> Optional[List[Attribute]]:
        """
        Get a dict of attributes and values
        """
        attributes: List[dict] = []
        for attribute in self.attributes:
            attributes.append(attribute.dict(by_alias=True))
        return attributes

    def get_attribute_names(self) -> List[str]:
        """
        Get a list of attribute names
        """
        attribute_names: List[str] = []
        for attribute in self.attributes:
            attribute_names.append(attribute.attribute_name)
        return attribute_names
    
    def count(self) -> int:
        """
        Get the number of attributes
        """
        return len(self.attributes)

    def __len__(self) -> int:
        """
        Get the number of attributes
        """
        return len(self.attributes)

    def __iter__(self) -> Iterator[Attribute]:
        """
        Iterate through the attributes
        """
        return iter(self.attributes)

    def __getitem__(self, index: int) -> Attribute:
        """
        Get an attribute by index
        """
        return self.attributes[index]

    def __repr__(self) -> str:
        """
        Get a string representation of the attributes
        """
        return str(self.attributes)

    def __str__(self) -> str:
        """
        Get a string representation of the attributes
        """
        return str(self.attributes)