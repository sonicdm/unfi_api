from dateutil.parser import parse as date_parser
from datetime import date, datetime


def currency_string_to_float(currency: str) -> float:
    """
    Converts a string to a float.
    Removing all currency symbols and commas.
    """
    currency = str(currency)
    currency = currency.replace("$", "")
    # replace euro
    currency = currency.replace("€", "")
    # replace gbp
    currency = currency.replace("£", "")
    # replace deutsche mark
    currency = currency.replace("DM", "")
    # replace cent
    currency = currency.replace("¢", "")
    # replace yen
    currency = currency.replace("¥", "")
    # replace yuan
    currency = currency.replace("元", "")
    # replace rupee
    currency = currency.replace("₹", "")
    # replace dinar
    currency = currency.replace("د.إ", "")
    # replace peso
    currency = currency.replace("₱", "")
    # replace comma
    currency = currency.replace(",", "")
    if currency == "":
        return 0.0
    return float(currency)


def validate_date_input(date_val):
    """
    Converts a string to a date.
    """

    if not isinstance(date_val, (str, date, datetime)):
        return None
    if isinstance(date_val, str):
        return date_parser(date_val)
    if isinstance(date_val, date):
        return date_val
    elif isinstance(date_val, datetime):
        return date_val.date()
