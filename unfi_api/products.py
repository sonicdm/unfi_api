import inspect
import re
from datetime import date
from typing import Optional

from dateutil.parser import parse as date_parse
from pydantic import BaseModel, validator

from unfi_api.utils.string import strings_to_numbers


def camel_to_snake_case(s):
    regex = r"([a-z]+)([A-Z]+)"
    return re.sub(regex, r"\1_\2", s).lower()


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))


class UnfiObject(object):

    def __init__(self, **kwargs):
        if kwargs:
            self.create(kwargs)

    def create(self, d):
        for k, v in d.items():
            setattr(self, camel_to_snake_case(k).lstrip("_"), v)


class Product(object):

    def __init__(
            self, product=None, product_data=None, product_detail=None, marketing=None, ingredients=None,
            nutrition_facts=None,
            attributes=None, pricing=None
    ):
        # Identifiers
        self.product_code = None
        self.product_int_id = None
        self.product_number = None
        self.upc = None
        self.master_case_upc = None
        self.inner_case_upc = None
        self.plu = None
        self.substitute_number = None

        # Descriptions
        self.department_id = None
        self.brand_id = None
        self.brand_name = None
        self.category_id = None
        self.category_name = None
        self.product_name = None
        self.short_description = None
        self.long_description = None
        self.sub_header = None
        self.sub_header_id = None
        self.size = None
        self.pack_size = None
        self.unit_type = None
        self.units_in_full_case = None
        self.speciality_flag = None
        self.organic_code = None
        self.country_of_origin_id = None
        self.country_of_origin_name = None

        # Pricing & Availability
        # self.stock_avail = None
        # self.stock_oh = None
        self.discount = None
        self.per_unit_price = None
        self.price = None
        self.minimum_order_quantity = None
        self.minqty = None

        # Image Info
        self.image_available = None
        self.img_file_name = None
        self.img_url = None
        self.is_image_available = None

        # Unused
        self.search_keywords = None
        self.is_new = None
        self.is_private_label = None
        self.is_sponsored = None
        self.private_lbl_dept = None
        self.product_owner = None
        self.pvlabel_code = None
        self.total_rows = None
        self.warehouse_message = None
        self.created_by = None
        self.created_date = None
        self.modified_by = None
        self.modified_date = None
        self.is_active = None
        self.is_deleted = None
        self.requires_customer_authorization = None
        self.member_applicable_fee = None
        self.division_code = None

        # Objects
        self._attributes = []
        self.marketing = None
        self.ingredients = None
        self.nutrition_facts = None
        self._pricing = None

        # Protected Attributes
        self.__stock_avail = None
        self.__stock_oh = None
        self.__upc = None
        self.__master_case_upc = None
        self.__inner_case_upc = None

        if product:
            self.from_dict(product)
        if product_data:
            self.from_dict(product_data)
        if product_detail:
            self.from_dict(product_detail)
        if attributes:
            for attribute in attributes:
                self._attributes.append(Attribute(**attribute))
        if ingredients:
            self.ingredients = Ingredients(**ingredients)
        if marketing:
            self.marketing = Marketing(**marketing)
        if nutrition_facts:
            self.nutrition_facts = NutritionFacts(nutrition_facts)
        if pricing:
            self._pricing = Pricing(pricing)

        pass

    def from_dict(self, d):
        for k, v in d.items():
            setattr(self, camel_to_snake_case(k), strings_to_numbers(v))
            # print("self.%s = None" % camel_to_snake_case(k))

    @property
    def stock_oh(self):
        return self.__stock_oh

    @stock_oh.setter
    def stock_oh(self, value):
        if self.__stock_oh:
            if abs(self.__stock_oh) < abs(value):
                self.__stock_oh = value
        else:
            self.__stock_oh = value

    @property
    def stock_avail(self):
        return self.__stock_avail

    @stock_avail.setter
    def stock_avail(self, value):
        if self.__stock_avail:
            if abs(self.__stock_avail) < abs(value):
                self.__stock_avail = value
        else:
            self.__stock_avail = value

    @property
    def upc(self):
        return self.__upc

    @upc.setter
    def upc(self, value):
        if value:
            if isinstance(value, str):
                value = re.sub(r"\W", "", value)
            self.__upc = int(value)

    @property
    def master_case_upc(self):
        return self.__master_case_upc

    @master_case_upc.setter
    def master_case_upc(self, value):
        if value:
            self.__master_case_upc = int(value)

    @property
    def inner_case_upc(self):
        return self.__inner_case_upc

    @inner_case_upc.setter
    def inner_case_upc(self, value):
        if value:
            self.__inner_case_upc = int(value)

    @property
    def pricing(self):
        return list(self._pricing)

    def update(self, d):
        self.from_dict(d)

    def get_values(self):
        out = {}
        for k, v in inspect.getmembers(self):
            if not str(k).startswith("_") and not callable(v):
                out[k] = v
        return out

    def __repr__(self):

        items = {
            "brand": self.brand_name,
            "long_description": self.long_description,
            "short_description": self.short_description,
            "size": self.size,
            "pack_size": self.pack_size,
        }

        items = ("%s = %r" % (k, v) for k, v in self.get_values().items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))


class Pricing(object):

    def __init__(self, result=None):
        self.costs = []

        if result:
            self.add_costs(result)

    def add_cost(self, cost_record):
        self.costs.append(Cost(**cost_record))

    def add_costs(self, cost_records):
        for record in cost_records:
            self.add_cost(record)

    def __iter__(self):
        for cost in self.costs:
            yield cost.get_values()


class Cost(UnfiObject):
    def __init__(self, **kwargs):
        # self.product_code = product_code
        self.__price_reason = None
        self.price_type = None
        self.min_qty = None
        self.discount_amount = None
        self.discount_sign = None
        self.net_flag = None
        self.case_savings = None
        self.each_savings = None
        self.__start_date = None
        self.__end_date = None
        self.__case_price = None
        self.__unit_price = None
        self.__retail_price = None
        self.margin = None
        super().__init__(**kwargs)

    @property
    def price_reason(self):
        return self.__price_reason

    @price_reason.setter
    def price_reason(self, val):
        self.__price_reason = val if val else "R"

    @property
    def case_price(self):
        return self.__case_price

    @case_price.setter
    def case_price(self, value):
        self.__case_price = float(str(value).replace("$", ""))

    @property
    def unit_price(self):
        return self.__unit_price

    @unit_price.setter
    def unit_price(self, value):
        self.__unit_price = float(str(value).replace("$", ""))

    @property
    def retail_price(self):
        return self.__retail_price

    @retail_price.setter
    def retail_price(self, value):
        self.__retail_price = float(str(value).replace("$", ""))

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value):
        if not all(x in ["0", "/"] for x in value):
            self.__start_date = date_parse(value).date()

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, value):
        if not all(x in ["0", "/"] for x in value):
            self.__end_date = date_parse(value).date()

    def get_values(self):
        out = {}
        for k, v in inspect.getmembers(self):
            if not str(k).startswith("_") and not callable(v):
                out[k] = v
        return out

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))


class Attribute(UnfiObject):
    def __init__(self, **kwargs):
        self.attribute_id = None
        self.attribute_name = None
        self.source_of_attribute_data = None
        self.created_by = None
        self.created_date = None
        self.modified_by = None
        self.modified_date = None
        self.active = None
        super().__init__(**kwargs)

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))


class Attributes:

    def __init__(self, **kwargs):
        pass


class Marketing(object):

    def __init__(self, **kwargs):
        self.__advertising_text = None
        self.__advertising_description = None
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, camel_to_snake_case(k), v)

    @property
    def advertising_text(self):
        return self.__advertising_text

    @advertising_text.setter
    def advertising_text(self, value):
        if isinstance(value, str):
            self.__advertising_text = value.strip().title()

    @property
    def advertising_description(self):
        return self.__advertising_description

    @advertising_description.setter
    def advertising_description(self, value):
        if isinstance(value, str):
            self.__advertising_description = value.strip().title()


class NutritionFacts:
    """
    representation of nutrition Facts
    """

    def __init__(self, results=None):
        self.nutrients = []
        self.calories = None
        self.calories_from_fat = None
        self.serving_size = None
        self.servings_per_container = None
        if results:
            self.add_nutrients(results)

    def add_nutrient(self, d):
        nutrient_name = d.get('NutrientName')
        if nutrient_name == 'fromFat':
            self.calories_from_fat = d.get('Amount')
        elif nutrient_name == 'calories':
            self.calories = d.get('Amount')
        elif nutrient_name == 'servingsContainer':
            self.servings_per_container = d.get('Amount')
        elif nutrient_name == 'servingSize':
            self.serving_size = d.get('Amount')
        else:
            nutrient = Nutrient(**d)
            self.nutrients.append(nutrient)

    def add_nutrients(self, result):
        for nutrient in result:
            self.add_nutrient(nutrient)

    @property
    def values(self):
        output = {}
        for nutrient in self.nutrients:
            if nutrient.amount:
                output[nutrient.name] = {
                    'amount': nutrient.amount,
                    'unit': nutrient.unit,
                    'dv': nutrient.percent_dv
                }
        return output

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))


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


class Ingredients(BaseModel):
    ingredients: Optional[str]
    modified_date: Optional[date]

    class Config:
        alias_generator = to_camel

    @validator("modified_date", pre=True)
    def parse_date_string(cls, v):
        if isinstance(v, str):
            return date_parse(v).date()
