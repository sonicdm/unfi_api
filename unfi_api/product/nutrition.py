from datetime import date
from dateutil.parser import parse as date_parse
from pydantic import validator, root_validator
from pydantic.utils import to_camel
from typing import Optional, List, Dict, Any
import re
from pydantic.main import BaseModel

from unfi_api.utils import string_to_snake


class Nutrient(BaseModel):
    """
    Data model for unfi nutition facts
    """

    nutrient_name: Optional[str]
    nutrition_fact_id: Optional[str]
    product_int_id: Optional[str]
    nutrient_id: Optional[str]
    amount: Optional[str]
    percent_dv: Optional[str]
    label_order: Optional[str]
    created_by: Optional[str]
    created_date: Optional[date]
    modified_by: Optional[str]
    modified_date: Optional[date]
    active: Optional[str]
    display_panel: Optional[str]
    display_panel_new: Optional[str]
    nutrient: Optional[str]

    UNIT_MAP = {
        'iron': '%',
        'calcium': '%',
        'vitaminC': '%',
        'vitaminA': '%',
        'protein': 'g',
        'sugars': 'g',
        'dietaryFiber': 'g',
        'totalCarbs': 'g',
        'sodium': 'mg',
        'transFat': 'g',
        'saturatedFat': 'g',
        'totalFat': 'g',
        'cholesterol': 'mg',
        'addedSugar': 'g',
        'potassium': 'g',
    }

    class Config:
        alias_generator = to_camel

    @validator("modified_date", "created_date", pre=True)
    def parse_date_string(cls, v):
        if isinstance(v, str):
            return date_parse(v).date()

    @property
    def name(self):
        if self.nutrient_name:
            return re.sub(r"([a-z]+)([A-Z]+)", r"\1 \2", self.nutrient_name).title()
        else:
            return None

    @property
    def unit(self):
        return self.UNIT_MAP.get(self.nutrient_name)

    def __str__(self):
        return str({
            'name': self.nutrient_name,
            'amount': self.amount,
            'unit': self.unit,
            'dv': self.percent_dv
        })


class NutritionFacts(BaseModel):
    """
    BaseModel representation of NutritionFacts from an api nutrition_facts call
    non member attributes are turned into nutrients
    """
    nutrients: Optional[List[Nutrient]]
    calories: Optional[int]
    calories_from_fat: Optional[int]
    serving_size: Optional[str]
    servings_container: Optional[str]

    # # nutrients: Optional[List[Nutrient]] = []
    # nutrition_facts: Optional[List[Nutrient]] = []
    # calories: Optional[int]
    # from_fat: Optional[int]
    # serving_size: Optional[str]
    # servings_container: Optional[str]

    # def add_nutrition_fact(self, nutrition_fact: Dict[str, Any]) -> None:
    #     name = string_to_snake(nutrition_fact["nutrientName"])
    #     # if nutrients name converted to snake case is in member variables set them otherwise create nutrition fact
    #     if name in self.__dict__:
    #         if name == "from_fat":
    #             self.calories_from_fat = nutrition_fact["amount"]
    #         else:
    #             setattr(self, name, nutrition_fact["amount"])
    #     else:
    #         self.nutrients.append(Nutrient(**nutrition_fact))

    # get nutrition fact values as a dictionary including calories, calories from fat serving information
    @root_validator(pre=True)
    def get_nutrition_facts(cls, values):
        nutrition_facts: List[Nutrient] = []
        for nutrition_fact in values["nutrients"]:
            nutrient = Nutrient(**nutrition_fact)
            if nutrient.nutrient_name == "calories":
                values['calories'] = nutrient.amount
            elif nutrient.nutrient_name == "fromFat":
                values['calories_from_fat'] = nutrient.amount
            elif nutrient.nutrient_name == "servingSize":
                values['serving_size'] = nutrient.amount
            elif nutrient.nutrient_name == "servingsContainer":
                values['servings_container'] = nutrient.amount
            else:
                nutrition_facts.append(nutrient)

        values["nutrients"] = nutrition_facts
        # del values["__root__"]
        return values

    @property
    def nutrition_facts(self) -> List[Dict[str, Any]]:
        nutrition_facts = []
        for member in self.__dict__:
            if member != "nutrients":
                nutrition_facts.append({f"{member}": f"{getattr(self, member)}"})
        for nutrition_fact in self.nutrients:
            nutrition_facts.append(nutrition_fact.dict())
        return nutrition_facts

    # print nutrition facts property as a table
    def as_table(self) -> str:
        nutrition_facts = self
        nutrition_facts_table = ""
        # append class member variables excluding nutrition facts list
        for member in self.__dict__:
            if member != "nutrients":
                nutrition_facts_table += f"{member}: {getattr(self, member)}\n"
        # append nutrition facts list
        for nutrition_fact in self.nutrients:
        
            nutrition_facts_table += f"{nutrition_fact.name}: {nutrition_fact.amount} {nutrition_fact.unit} {nutrition_fact.percent_dv}% dv\n"

        return nutrition_facts_table
