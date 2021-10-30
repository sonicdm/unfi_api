from dateutil.parser import parse as date_parser


def currency_string_to_float(currency:str)->float:
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


def string_to_date(date):
    """
    Converts a string to a date.
    """
    date_ = date_parser(date)
    return date_.date()
