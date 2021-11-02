from datetime import date
from typing import Any, Dict, List, Optional, Union

from bs4 import BeautifulSoup
from pydantic import Field, validator
from pydantic.class_validators import root_validator
from pydantic.main import BaseModel

from unfi_api.utils import (
    isnumber,
)
from unfi_api.utils.string import strings_to_numbers, camel_to_snake_case, remove_escaped_characters
from unfi_api.validators import currency_string_to_float, validate_date_input

price_types = {
    "A": "Customer Specific Ad Program",
    "C": "Specialty Discount",
    "E": "Every Day Low Price (EDLP)",
    "F": "Circular Deal",
    "H": "HABA Discount",
    "M": "Super Saver Deals & New Additions",
    "N": "Net Deal / Net Restricted",
    "P": "Price Promotion",
    "S": "Customer Specific Shelf Sale",
    "Z": "Every Day Low Cost (EDLC)",
    "R": "Retail",
}


def parse_pricing(response_content):
    response_content = remove_escaped_characters(response_content)
    promo_soup = BeautifulSoup(response_content, "html.parser")
    # find table that contains the pricing.
    promo_table = promo_soup.find_all("table")[1]
    promo_rows = []
    promo_headers = [
        header.text.replace(" ", "_").replace(".", "").lower()
        for header in promo_table.find_all("th")
    ]
    # promo_rows.append(promo_headers)
    # grab table values and put into lists
    for row in promo_table.find_all("tr"):
        cur_row = []
        for cell in row.find_all("td"):
            cur_row.append(strings_to_numbers(cell.get_text().strip().replace("$", "")))
        if len(cur_row) == len(promo_headers):
            promo_rows.append(dict(zip(promo_headers, cur_row)))

    # create pricing data
    pricing: Dict[str, Any] = {}
    costs: Dict[str, dict] = {}
    for row in promo_rows:
        """
        row = {'price_reason': '', 'min_qty': 1, 'discount_amount': '', 'discount_sign': '', 'net_flag': '',
        'case_savings': '', 'each_savings': '', 'start_date': '00/00/0000', 'end_date': '00/00/0000',
        'case_price': 27.24, 'unit_price': 4.54, 'retail_price': 6.99, 'margin': '35.05%'}
        """
        price_type = row["price_reason"]
        cost = {}
        if not price_type:
            price_type = "R"
            pricing["case_price"] = currency_string_to_float(row["case_price"])
            pricing["unit_price"] = currency_string_to_float(row["unit_price"])
            pricing["retail_margin"] = float(row["margin"].replace("%", "")) / 100
            pricing["retail_price"] = currency_string_to_float(row["retail_price"])

        cost["price_type"] = price_type
        cost["price_description"] = price_types[price_type]
        cost["min_qty"] = row["min_qty"]
        cost["discount_amount"] = currency_string_to_float(row["discount_amount"])
        cost["discount_sign"] = row["discount_sign"]
        cost["net_flag"] = row["net_flag"]
        cost["case_savings"] = currency_string_to_float(row["case_savings"])
        cost["each_savings"] = currency_string_to_float(row["each_savings"])
        cost["start_date"] = (
            row["start_date"] if row["start_date"] not in ["", "00/00/0000"] else None
        )
        cost["end_date"] = (
            row["end_date"] if row["end_date"] not in ["", "00/00/0000"] else None
        )
        cost["case_price"] = currency_string_to_float(row["case_price"])
        cost["unit_price"] = currency_string_to_float(row["unit_price"])
        cost["retail_price"] = currency_string_to_float(row["retail_price"])
        cost["margin"] = float(row["margin"].replace("%", "")) / 100
        costs[price_type] = cost
    pricing["costs"] = costs
    return pricing


class Cost(BaseModel):
    """
    Cost record of a product with detailed information
    """

    price_type: str
    price_description: str
    min_qty: int
    discount_amount: float
    discount_sign: str
    net_flag: str
    case_savings: float
    each_savings: float
    start_date: Optional[date]
    end_date: Optional[date]
    case_price: float
    unit_price: float
    retail_price: float
    margin: float

    # class Options:
    #     arbitrary_types_allowed = True
    # validators
    _validate_date = validator("start_date", "end_date", pre=True, allow_reuse=True)(
        validate_date_input
    )

    @validator("case_price", "unit_price", "retail_price", pre=True, allow_reuse=True)
    def validate_price(cls, v):
        """remove currency symbol from price and convert to float"""
        if not isinstance(v, float):
            return float(str.v.replace("$", ""))
        return v
    



class Pricing(BaseModel):
    case_price: float
    unit_price: float
    retail_margin: float
    retail_price: float
    costs: Dict[str, Cost]

    def costs_to_dict(self) -> Dict[str, Any]:
        """
        Converts a list of costs to a dict of costs
        """
        costs = {}
        for cost in self.costs.values():
            for cost_field,cost_value in cost.dict(include={"case_price","unit_price","start_date","end_date"}).items():
                if cost.price_type == "R":
                    costs[cost_field] = cost_value
                else:
                    costs[f"{cost.price_type}_{cost_field}"] = cost_value
        return costs
