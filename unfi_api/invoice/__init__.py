from bs4 import BeautifulSoup
from bs4.element import ResultSet
from pydantic import BaseModel, validator, Field
from datetime import datetime, date
from typing import Any, Dict, Optional, List
from .line_item import LineItem
from lxml import etree
import re


def get_invoice_html_tables(invoice_xml: str) -> Dict[str, List[List[str]]]:
    """
    Get the table data from all tables in the invoice html.
    Clean up the input html extra returns and spaces
    """

    invoice_xml = invoice_xml.replace("\n", "").replace("\r", "").replace("\t", "")
    xml_soup = BeautifulSoup(invoice_xml, "lxml")
    invoice_data = {}
    invoice_tables = xml_soup.select('table')

    # Get the shipping table
    shipping_table = invoice_tables[1]
    invoice_data['shipping detail'] = get_table_data(shipping_table)

    # Get the billing table
    billing_table = invoice_tables[2]
    invoice_data['billing detail'] = get_table_data(billing_table)

    # Get the customer table
    customer_table = invoice_tables[5]
    invoice_data['customer detail'] = get_table_data(customer_table)

    # Get the Line Items table
    line_items_table = invoice_tables[6]
    invoice_data['line items'] = get_table_data(line_items_table)

    # Get the freight details table
    freight_details_table = invoice_tables[8]
    invoice_data['freight details'] = get_table_data(freight_details_table)

    # Get the invoice summary table
    invoice_summary_table = invoice_tables[9]
    invoice_data['invoice summary'] = get_table_data(invoice_summary_table)

    return invoice_data


def get_table_data(table_soup: ResultSet) -> List[List[str]]:
    """
    Get the table data from the table ResultSet.
    """
    table_data = []
    table_rows = table_soup.find_all('tr')
    for row in table_rows:
        row_data = []
        row_cells = row.find_all('td')
        for cell in row_cells:
            row_data.append(cell.text)
        table_data.append(row_data)
    return table_data


def parse_table_with_labels_on_left(table_data: List[List[str]]) -> Dict[str, str]:
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
        line_item_dict[int(ln['LN'])] = ln

    return line_item_dict


class Invoice(BaseModel):
    """
    Invoice object
    collection of invoice information and line items.
    """
    # Invoice Details
    customer: str = Field(alias='Customer')
    invoice_number: str = Field(alias='Invoice Number')
    invoice_date: date = Field(alias='Invoice Date')
    delivery_date: date = Field(alias='Delivery Date')
    terms: str = Field(alias='Terms')
    master: str = Field(alias='Master')
    ordered_on: date = Field(alias='Ordered On')
    purchase_order: str = Field(alias='Purchase Order')

    # Shipping Details
    weight: float = Field(alias='Weight')
    cubes: float = Field(alias='Cubes')
    cases: int = Field(alias='Cases')
    subtotal: float = Field(alias='Subtotal')
    discount: float = Field(alias='Discount')

    # Cost Details
    tax: float = Field(alias='Tax')
    freight: float = Field(alias='Freight')
    fuel_surcharge: float = Field(alias='Fuel Surcharge')
    redempt: float = Field(alias='Redempt')
    credit_allowance: float = Field(alias='Credit Allowance')
    total: float = Field(alias='Total')

    # Line Items
    line_items: Dict[int, Any] = []  # line number: LineItem
    out_of_stock_items: List[Any] = []
    shorted_items: List[Any] = []

    @validator('invoice_date', 'delivery_date')
    def date_validator(cls, v):
        """convert date string to datetime.date"""
        return datetime.strptime(v, '%m/%d/%Y').date()

    def add_line_item(self, line_item: LineItem):
        """Add line items to invoice. Add out of stock items to out of stock. Add shorted Items to shorted items."""
        self.line_items[LineItem.line_number] = line_item
        if line_item.shipped == 0:
            self.out_of_stock_items.append(line_item)
        elif line_item.shipped < line_item.ordered:
            self.shorted_items.append(line_item)
