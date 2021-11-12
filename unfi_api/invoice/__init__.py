from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from bs4 import BeautifulSoup
from bs4.element import ResultSet
from pydantic import BaseModel, Field, validator
from pydantic.class_validators import root_validator
from unfi_api import settings
from unfi_api.invoice.line_item import LineItem, LineItems
from unfi_api.utils.collections import normalize_dict, table_to_dicts
from unfi_api.utils.string import remove_escaped_characters
from unfi_api.validators import currency_string_to_float, validate_date_input

if TYPE_CHECKING:
    from unfi_api import UnfiApiClient

"""
    1: Invoices
    2: Web Orders
    4: Credits
    """
INVOICE = 1
WEB_ORDER = 2
CREDIT = 4


def make_invoice_table_soup(html: str) -> BeautifulSoup:
    """
    Make a soup object from the html
    """
    invoice_soup = BeautifulSoup(html, settings.beautiful_soup_parser)
    return invoice_soup.select("table")


def get_invoice_html_tables(invoice_xml: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get the table data from all tables in the invoice html.
    Clean up the input html extra returns and spaces
    """

    invoice_xml = invoice_xml.replace("\n", "").replace("\r", "").replace("\t", "")
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
            if not row[0].strip() and row[1].strip() and label != "":
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
    to: str = Field(..., alias="To:")
    address: str = Field(..., alias="Address:")
    city: str = Field(..., alias="City:")
    state: str = Field(..., alias="State:")
    zip_code_: str = Field(..., alias="Zip Code:")


class BillingDetail(BaseModel):
    to: str = Field(..., alias="To:")
    address: str = Field(..., alias="Address:")
    city: str = Field(..., alias="City:")
    state: str = Field(..., alias="State:")
    zip_code: str = Field(..., alias="Zip Code:")


class FreightDetails(BaseModel):
    weight: str = Field(..., alias="Weight:")
    cubes: str = Field(..., alias="Cubes:")
    cases: str = Field(..., alias="Cases:")


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
    )(validate_date_input)

    def normalize(self):
        """
        Normalize the invoice data.
        """
        return normalize_dict(self.dict())
    
    def __str__(self) -> str:
        return f"Invoice(date: {self.invoice_date}, invoice_number: {self.invoice_number}, total_items: {len(self.line_items)}, Total: ${self.total})"
    
    def __repr__(self) -> str:
        return str(self)


class OrderListing(BaseModel):
    # total_rows: int = Field(..., alias='Total_Rows')
    # row_number: int = Field(..., alias='Row_Number')
    invoice_number: str = Field(..., alias='InvoiceNumber')
    invoice_date: date = Field(..., alias='InvoiceDate')
    order_number: str = Field(..., alias='OrderNumber')
    requested_date: date = Field(..., alias='RequestedDate')
    requested_by: str = Field(..., alias='RequestedBy')
    status: Optional[str] = Field(..., alias='Status')
    po_number: str = Field(..., alias='PONumber')
    pk_key: str = Field(..., alias='PKKey')
    dollar_total: float = Field(..., alias='DollarTotal')
    cases_shipped: float = Field(..., alias='CasesShipped')
    weight_shipped: float = Field(..., alias='WeightShipped')

    _date_validator = validator(
        "invoice_date", "requested_date", allow_reuse=True, pre=True
    )(validate_date_input)


class OrderList(BaseModel):
    __root__: Optional[Dict[str, OrderListing]] = {}

    @root_validator(pre=True)
    def listing_to_dict(cls, values):
        """
        Convert the order listing to a dict.
        """
        listings = values.get("__root__")
        if not listings:
            return values
        new_dict = {}
        if isinstance(listings, dict):
            for key, value in listings.items():
                if isinstance(value, OrderListing) and isinstance(key, str):
                    new_dict[key] = value.dict()
                elif isinstance(value, dict) and isinstance(key, str):
                    new_dict[str(key)] = value
                    
                else:
                    raise ValueError(
                        "Invalid OrderListing object. "
                        "Expected OrderListing or dict, got {}".format(type(value))
                    )
            return values
        for listing in listings:
            if isinstance(listing, OrderListing):
                new_dict[listing.invoice_number] = listing.dict()
            else:
                if "InvoiceNumber" in listing:
                    new_dict[listing.get("InvoiceNumber")] = listing
                elif "invoice_number" in listing:
                    new_dict[listing.get("invoice_number")] = listing
                    
        values["__root__"] = new_dict
        return values

    @property
    def total_orders(self):
        return len(self.__root__)

    @property
    def orders(self) -> Dict[str, OrderListing]:
        return self.__root__

    def orders_by_date(self) -> Dict[date, List[OrderListing]]:
        """
        Return a dict indexed by invoice date
        """
        invoices: Dict[date, List[OrderListing]] = {}
        for invoice_number, listing in self.orders.items():
            invoice_date = listing.invoice_date
            if invoice_date not in invoices:
                invoices[invoice_date] = []
            invoices[invoice_date].append(listing)
        return invoices

    def filter_by_date(self, start_date: date, end_date: date) -> OrderList:
        """
        Filter the order list by date.
        """
        orders = OrderList()
        for order in self.orders.values():
            if start_date <= order.invoice_date <= end_date:
                orders.add_order(order)

        return orders
    
    def add_order(self, order: Union[OrderListing,OrderList]):
        """
        Add an order to the order list.
        """
        if isinstance(order, OrderList):
            self.__root__.update(order.orders)
        
        else:
            self.__root__[order.invoice_number] = order    
    
    def download_orders(self, client: 'UnfiApiClient'):
        """
        Download the orders from the API.
        """
        ...
        
    def __iter__(self):
        return iter(self.__root__.values())

    def __getitem__(self, invoice_number):
        return self.__root__[invoice_number]
    
    def values(self):
        return self.__root__.values()
    
    def items(self):
        return self.__root__.items()
    
    def keys(self):
        return self.__root__.keys()
    
    def __add__(self, other):
        # if other is not an OrderList, OrderListing,
        # not list of OrderList, OrderListing or dicts, raise add not supported
        if isinstance(other, OrderList):
            self.__root__.update(other.__root__)
        elif isinstance(other, OrderListing):
            self.__root__[other.invoice_number] = other
        elif isinstance(other, list):
            if all(isinstance(item, OrderListing) for item in other) or all(isinstance(item, OrderList) for item in other):
                for listing in other:
                    self.add_order(listing)
        else:
            raise TypeError("unsupported operand type(s) for +: 'OrderList' and '{}'".format(type(other)))

    def __len__(self):
        return len(self.__root__)
    