from bs4 import BeautifulSoup
from bs4.element import ResultSet
from pydantic import BaseModel, validator, Field
from datetime import date
from typing import Any, Dict, List
from .line_item import LineItem, LineItems

from unfi_api.utils import table_to_dicts, remove_escaped_characters, normalize_dict
from unfi_api.validators import currency_string_to_float, string_to_date


def make_invoice_table_soup(html: str) -> BeautifulSoup:
    """
    Make a soup object from the html
    """
    invoice_soup = BeautifulSoup(html, "lxml")
    return invoice_soup.select("table")


def get_invoice_html_tables(invoice_xml: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get the table data from all tables in the invoice html.
    Clean up the input html extra returns and spaces
    """

    invoice_xml = invoice_xml.replace("\n", "").replace("\r", "").replace("\t", "")
    xml_soup = BeautifulSoup(invoice_xml, "lxml")
    invoice_data = {}
    invoice_tables = make_invoice_table_soup(invoice_xml)

    # Get the shipping table
    shipping_table = invoice_tables[1]
    shipping_detail = get_table_data(shipping_table)
    invoice_data["shipping detail"] = parse_table_with_labels_on_left(shipping_detail)

    # Get the billing table
    billing_table = invoice_tables[2]
    billing_detail = parse_table_with_labels_on_left(get_table_data(billing_table))
    invoice_data["billing detail"] = billing_detail

    # # Get the customer table
    # customer_table = invoice_tables[5]
    # invoice_data["customer detail"] = parse_table_with_labels_on_left(
    #     get_table_data(customer_table)
    # )

    # Invoice details
    invoice_detail_table = invoice_tables[5]
    invoice_detail = table_to_dicts(get_table_data(invoice_detail_table))
    invoice_data.update(invoice_detail[0])

    # Get the Line Items table
    line_items_table = invoice_tables[6]
    invoice_data["line items"] = table_to_dicts(get_table_data(line_items_table))

    # Get the freight details table
    freight_details_table = invoice_tables[8]
    invoice_data["freight details"] = parse_table_with_labels_on_left(
        get_table_data(freight_details_table)
    )

    # Get the invoice summary table
    invoice_summary_table = invoice_tables[9]
    invoice_summary = parse_table_with_labels_on_left(
        get_table_data(invoice_summary_table)
    )
    invoice_data.update(invoice_summary)
    return invoice_data


def get_table_data(table_soup: ResultSet) -> List[List[str]]:
    """
    Get the table data from the table ResultSet.
    """
    table_data = []
    table_rows = table_soup.find_all("tr")
    for row in table_rows:
        row_data = []
        row_cells = row.find_all("td")
        for cell in row_cells:
            row_data.append(remove_escaped_characters(cell.text).strip())
        table_data.append(row_data)
    return table_data


def parse_table_with_labels_on_left(table_data: List[List[str]]) -> Dict[str, Any]:
    """
    Parse the invoice data with labels on the left. append to previous data if no label on left.
    """
    invoice_data = {}
    label = ""
    # invoice_data['tableName'] = table_data[0][0]
    for row in table_data:
        if len(row) == 2:
            if not row[0].strip() and row[1].strip() and label is not "":
                invoice_data[label] += "\n" + row[1]
            else:
                label = row[0].strip()
                invoice_data[label] = row[1].strip()
    return invoice_data


def index_line_item_table(line_items: List[List[str]]) -> Dict[int, Dict[str, str]]:
    """
    Store line items using the line number. use the first row as the index
    """
    line_item_dict = {}

    if not len(line_items) > 0:
        return line_item_dict

    header_row = [x.strip() for x in line_items[0]]
    for row in line_items[1:]:
        ln = dict(zip(header_row, [x.strip() for x in row]))
        line_item_dict[int(ln["LN"])] = ln

    return line_item_dict


class ShippingDetail(BaseModel):
    to_: str = Field(..., alias="To:")
    address_: str = Field(..., alias="Address:")
    city_: str = Field(..., alias="City:")
    state_: str = Field(..., alias="State:")
    zip__code_: str = Field(..., alias="Zip Code:")


class BillingDetail(BaseModel):
    to_: str = Field(..., alias="To:")
    address_: str = Field(..., alias="Address:")
    city_: str = Field(..., alias="City:")
    state_: str = Field(..., alias="State:")
    zip__code_: str = Field(..., alias="Zip Code:")


class FreightDetails(BaseModel):
    weight_: str = Field(..., alias="Weight:")
    cubes_: str = Field(..., alias="Cubes:")
    cases_: str = Field(..., alias="Cases:")


class Invoice(BaseModel):
    """
    Invoice object
    collection of invoice information and line items.
    """

    shipping_detail: ShippingDetail = Field(..., alias="shipping detail")
    billing_detail: BillingDetail = Field(..., alias="billing detail")
    customer: str = Field(..., alias="Customer")
    invoice_number: str = Field(..., alias="Invoice Number")
    invoice_date: date = Field(..., alias="Invoice Date")
    delivery_date: date = Field(..., alias="Delivery Date")
    terms: str = Field(..., alias="Terms")
    master: str = Field(..., alias="Master")
    ordered_on: date = Field(..., alias="Ordered On")
    purchase_order: str = Field(..., alias="Purchase Order")
    line_items: LineItems = Field(..., alias="line items")
    freight_details: FreightDetails = Field(..., alias="freight details")
    subtotal: str = Field(..., alias="Subtotal:")
    discount: str = Field(..., alias="Discount:")
    tax: str = Field(..., alias="Tax:")
    freight: str = Field(..., alias="Freight:")
    fuel_surcharge: str = Field(..., alias="Fuel Surcharge:")
    redempt: str = Field(..., alias="Redempt:")
    credit_allowance: str = Field(..., alias="Credit Allowance:")
    total: str = Field(..., alias="Total:")

    # validators
    _currency_to_float = validator(
        "subtotal",
        "discount",
        "tax",
        "freight",
        "fuel_surcharge",
        "redempt",
        "credit_allowance",
        "total",
        allow_reuse=True,
        pre=True,
    )(currency_string_to_float)
    _string_to_date = validator(
        "invoice_date", "delivery_date", "ordered_on", allow_reuse=True, pre=True
    )(string_to_date)

    def normalize(self):
        """
        Normalize the invoice data.
        """
        return normalize_dict(self.dict())
