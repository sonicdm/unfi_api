from datetime import date
from typing import Any, Dict

from bs4 import BeautifulSoup
from pydantic import Field, validator
from pydantic.main import BaseModel

from unfi_api.utils import strings_to_numbers, isnumber


def parse_pricing(response_content):
    promo_soup = BeautifulSoup(response_content, 'html.parser')
    # find table that contains the pricing.
    promo_table = promo_soup.find_all('table')[1]
    promo_rows = []
    promo_headers = [header.text for header in promo_table.find_all('th')]
    promo_rows.append(promo_headers)
    # grab table values and put into lists
    for row in promo_table.find_all('tr'):
        cur_row = []
        for cell in row.find_all('td'):
            cur_row.append(cell.get_text().replace('\\r', '').replace(
                '\\t', '').replace('\\n', '').strip())
        promo_rows.append(cur_row)
    promo_rows.remove([])

    # create pricing data
    pricing = {}

    for row in promo_rows[1:]:
        row = [strings_to_numbers(str(i).replace('$', '')) for i in row]
        price_type = row[0]
        if not price_type:
            pricing['retail_case_cost'] = row[-4]
            pricing['retail_unit_cost'] = row[-3]
            srp = row[-2]
            if isnumber(srp):
                pricing['retail_srp'] = row[-2]
                # pricing['retail_srp'] = simple_round_retail(row[-2])
            else:
                pricing['retail_srp'] = 0
            continue
        else:
            promo_price = row[-2]
            promo_case_cost = row[9]
            promo_unit_cost = row[10]
            promo_from = row[7]
            promo_to = row[8]
            promo_key = price_type + "_"
            pricing[promo_key + "srp"] = promo_price
            pricing[promo_key + "case_cost"] = promo_case_cost
            pricing[promo_key + "unit_cost"] = promo_unit_cost
            pricing[promo_key + "from"] = promo_from
            pricing[promo_key + "to"] = promo_to

    return pricing


class Cost(BaseModel):
    """
    Cost record of a product with detailed information
    """
    price_reason = Field(str, alias="Price Reason")
    price_type = Field(str, alias="Price Type")
    min_qty = Field(int, alias="Min. Qty.")
    discount_amount = Field(int, alias="Discount Amount")
    discount_sign = Field(str, alias="Discount Sign")
    net_flag = Field(str, alias="Net Flag")
    case_savings = Field(int, alias="Case Savings")
    each_savings = Field(int, alias="Each Savings")
    start_date = Field(date, alias="Start Date")
    end_date = Field(date, alias="End Date")
    case_price = Field(int, alias="Case Price")
    unit_price = Field(int, alias="Unit Price")
    retail_price = Field(int, alias="Retail Price")
    margin = Field(float, alias="Margin")

    class Options:
        arbitrary_types_allowed = True

    @validator("price_reason")
    def validate_price_reason(cls, v):
        """if no price reason, reason is R"""
        if not v:
            return "R"
        return v

    @validator("case_price", "unit_price", "retail_price")
    def validate_price(cls, v):
        """remove currency symbol from price and convert to float"""
        return float(v.replace("$", ""))


class Costs:
    """Collection for Cost objects contains dict of Cost Type: Cost Object"""

    def __init__(self, pricing_xml: str):
        self.costs: Dict[str, Cost] = {}
        self.pricing_xml = pricing_xml
        self.parsed_pricing: Dict[str, Any] = parse_pricing(pricing_xml)
    
    def get_cost(self, cost_type: str) -> Cost:
        """
        Returns a Cost object for a given cost type
        """
        return self.costs[cost_type]

    def get_cost_types(self) -> list:
        """
        Returns a list of cost types
        """
        return list(self.costs.keys())

    def costs_to_dict(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns a dict of cost types to dict of cost attributes
        """
        return {cost_type: cost.dict() for cost_type, cost in self.costs.items()}
        
    
    def __getitem__(self, key):
        return self.costs[key]

    def __setitem__(self, key, cost: Cost):
        self.costs[key] = cost
    
    def __iter__(self):
        return iter(self.costs)
    
    def __len__(self):
        return len(self.costs)

    def __repr__(self):
        return f"Costs({self.costs})"

    def __str__(self):
        return f"Costs({self.costs})"
    
    
