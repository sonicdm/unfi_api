import re
from string import hexdigits
from typing import Any, Iterable, Union


def clean_size_field(text: str) -> str:
    if not isinstance(text, str):
        return text
    size = text.split('/')
    if len(size) > 1:
        output = "/".join(size[1:])
        return output.strip()
    else:
        return size.pop().strip()


def is_hex(s: str) -> bool:
    """
    Check if a string is hexadecimal
    :param s: string
    :type s: str
    :return: bool
    :rtype: bool
    >>> is_hex('aavv22')
    False
    >>> is_hex('44dFa5')
    True
    """
    if not isinstance(s, str):
        return False
    s = s.replace('#', '')
    hex_digits = set(hexdigits)
    return all(c in hex_digits for c in s)


def is_hexcolor(s: str) -> bool:
    """
    >>> is_hexcolor('ff55ee')
    True
    >>> is_hexcolor('123')
    True
    >>> is_hexcolor('abab')
    False
    >>> is_hexcolor('FFEERR')
    False
    """
    s = s.replace('#', '')
    if is_hex(s):
        if len(s) == 3 or len(s) == 6:
            return True
        else:
            return False
    else:
        return False


def strings_to_numbers(l, fmt='float'):
    """
    Turn number string into the specified format from a list of values or a single string

    >>> strings_to_numbers(['1', 'a', '2.34', 3])
    [1, 'a', 2.34, 3]
    >>> strings_to_numbers('2.34')
    2.34
    >>> strings_to_numbers('Hi There')
    'Hi There'
    >>> strings_to_numbers('   123456')
    123456
    >>> strings_to_numbers(None)
    """

    def _convert(s):
        if not s:
            return s
        try:
            if float(s).is_integer():
                return int(float(s))
            else:
                return float(s)
        except (ValueError, TypeError):
            return s

    if not l:
        return l
    if hasattr(l, "__iter__") and not isinstance(l, (str, int)):
        o = []
        for i in l:
            o.append(_convert(i))
        return o
    else:
        return _convert(l)


def isnumber(s: Any, numtype=None) -> bool:
    """
    >>> isnumber('1.23')
    True
    >>> isnumber('String')
    False
    >>> isnumber(1.23)
    True
    >>> isnumber(1)
    True
    >>> isnumber('1')
    True
    >>> isnumber('123,456')
    True
    >>> isnumber(None)
    False

    :param s:
    :param numtype: specific type of number. 'float' or 'int'
    :return: bool
    """
    v = str(s).replace(',', '')
    if v.isdigit():
        return True
    else:
        try:
            float(v)
            return True
        except ValueError:
            return False


def convert_strings_to_number(v: Union[str, Iterable]):
    """
    Convert a string to an int or float if possible.
    """
    if isinstance(v, str):
        try:
            return int(v)
        except ValueError:
            try:
                return float(v)
            except ValueError:
                return v
    elif isinstance(v, Iterable):
        return [convert_strings_to_number(x) for x in v]
    else:
        return v


def is_a_number(v: Any) -> bool:
    """
    check if value is a number. Remove commas and other number formatting.
    """
    v = str(v).replace(',', '')
    if v.isdigit():
        return True
    else:
        try:
            float(v)
            return True
        except ValueError:
            return False


def camel_to_snake_case(s: str) -> str:
    regex = r"([a-z]+)([A-Z]+)"
    return re.sub(regex, r"\1_\2", s).lower()

def pascal_case_to_snake_case(s: str) -> str:
    """
    Convert a string to lower case snake case.
    convert TestString to test_string
    """
    if isinstance(s, str):
        s = re.split(r'(?<!^)(?=[A-Z])', s)

        return "_".join(s).lower()
    else:
        return s

def string_to_snake(s: str) -> str:
    """
    Converts a string to lower case snake case.
    """
    if isinstance(s, str):
        return s.lower().replace(' ', '_')
    else:
        return s


def remove_escaped_characters(s: str) -> str:
    """
    Remove newlines and tabs and returns from a string.
    """
    return re.sub(r'([\n\t\r]|[\\]+(n|t|r))', '', s)
