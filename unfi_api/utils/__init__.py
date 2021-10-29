from __future__ import print_function

import re

try:
    from past.builtins import unicode
except ImportError:
    unicode = unicode
import calendar
import datetime
import string
from collections import Counter, OrderedDict

from dateutil import parser


# Date Utils
def last_thursday(year, month):
    c = calendar.Calendar(firstweekday=calendar.SUNDAY)
    monthcal = c.monthdatescalendar(year, month)
    last_fri = [day for week in monthcal for day in week if
                day.weekday() == calendar.FRIDAY and
                day.month == month][-1]
    last_thurs = last_fri - datetime.timedelta(1)
    return last_thurs


def last_saturday(year, month):
    c = calendar.Calendar(firstweekday=calendar.SUNDAY)
    monthcal = c.monthdatescalendar(year, month)
    last_sunday = [day for week in monthcal for day in week if
                   day.weekday() == calendar.SUNDAY and
                   day.month == month][-1]
    last_sat = last_sunday - datetime.timedelta(1)
    return last_sat


def last_friday(year, month):
    c = calendar.Calendar(firstweekday=calendar.SUNDAY)
    monthcal = c.monthdatescalendar(year, month)
    last_sat = [day for week in monthcal for day in week if
                day.weekday() == calendar.SATURDAY and
                day.month == month][-1]
    last_fri = last_sat - datetime.timedelta(1)
    return last_fri


def fuzzy_date(datestr, verbose=False):
    dateobj = None
    for word in datestr.replace('_', ' ').replace('-', ' ').strip(' ').split(' '):
        try:
            dateobj = parser.parse(word)
            fname = datestr.lower()
            if dateobj.strftime('%B').lower() in fname \
                    or dateobj.strftime('%b').lower() in fname:
                if verbose:
                    print('{word} matched to {month:%B}'.format(
                        word=word, month=dateobj))
                break
        except ValueError:
            pass
    return dateobj


# Text Utils


def clean_size_field(text):
    if not isinstance(text, (str, unicode)):
        return text
    size = text.split('/')
    if len(size) > 1:
        output = "/".join(size[1:])
        return output.strip()
    else:
        return size.pop().strip()


def is_hex(s):
    # type: (str) -> bool
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
    hex_digits = set(string.hexdigits)
    return all(c in hex_digits for c in s)


def is_hexcolor(s):
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
    if is_hex(s):
        if len(s) == 3 or len(s) == 6:
            return True
        else:
            return False
    else:
        return False


# Number Utils
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
    if hasattr(l, "__iter__") and not isinstance(l, (str, unicode, int)):
        o = []
        for i in l:
            o.append(_convert(i))
        return o
    else:
        return _convert(l)


def isnumber(s, numtype=None):
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
    flt = False
    integer = False
    if isinstance(s, (str, unicode, bytes)):
        s = s.replace(',', '')
    try:
        if float(s).is_integer():
            integer = True
        if not float(s).is_integer():
            flt = True
    except (ValueError, TypeError):
        return False
    else:
        if numtype:
            if numtype == 'float' and flt:
                return True
            elif numtype == 'int' and integer:
                return True
        elif flt or integer:
            return True
        else:
            return False


def find_most_common_member(l):
    counts = Counter(l).most_common(1)
    if len(counts) > 0:
        return counts[0][0]


def round_retails(price):
    """
    round a number to the nearest x9 or x5
    for 0x numbers:
    <= .04 numbers. Round down to .99
    >= .05 numbers. Round up to .15

    >>> round_retails('1.23')
    1.25
    >>> round_retails(1)
    0.99
    >>> round_retails(1.76)
    1.75
    >>> round_retails(1.77)
    1.79
    >>> round_retails(2.03)
    1.99
    >>> round_retails(2.07)
    2.15
    >>> round_retails(1.9)
    1.89
    >>> round_retails(1.1)
    0.99
    >>> round_retails(0.7)
    0.69
    >>> round_retails(3.09)
    3.15
    >>> round_retails(1.62)
    1.59


    :param price: float value to round
    :return:
    """
    s = u"%s" % round(float(price), 2) if isnumber(price) else None
    if not s:
        raise TypeError('a number value is required')
    hund = None
    tenth = None
    whole = None
    if isnumber(price, 'float'):
        whl, dec = s.split('.')
        hund = int(dec[-1]) if len(dec) == 2 else 0
        tenth = int(s[-2]) if len(dec) == 2 else int(s[-1])
        whole = int(whl)
    elif isnumber(price, 'int'):
        hund = 0
        tenth = 0
        whole = int(price)

    if hund == 0:
        if tenth <= 1:
            if whole > 0:
                whole -= 1
            tenth = 9
            hund = 9
        else:
            tenth -= 1
            hund = 9

        return float("{}.{}{}".format(whole, tenth, hund))

    if hund not in [5, 9] or tenth == 0:

        if tenth == 0:
            if 4 < hund < 10:
                tenth = 1
                hund = 5
            if 0 < hund < 5:
                if 0 < whole < 5:
                    whole -= 1
                else:
                    whole = 0
                tenth = 9
                hund = 9

        if tenth > 4 and hund < 1:
            tenth = 9
            hund = 9

        if 2 < hund < 7:
            hund = 5

        if 0 < hund < 3:
            hund = 9
            if tenth <= 1:
                if whole > 0:
                    whole -= 1
                    tenth = 9
            else:
                tenth -= 1

        if 6 < hund < 10:
            hund = 9

        if 0 < hund < 3:
            whole -= 1
            hund = 9
            tenth = 9
        if hund == 0:
            whole -= 1
            tenth = 9
            hund = 9
        return float("{}.{}{}".format(whole, tenth, hund))
    else:
        return float(price)


# Collection Utils
def sort_dict(d):
    od = OrderedDict((k, v) for k, v in sorted(d.items()))
    return od


def is_cur_col(key, cur_cols):
    cur_cols = set(["%s".lower() % x for x in cur_cols])
    key = u"%s" % key
    return len(set(key.lower().split(' ')).intersection(cur_cols)) > 0


def index_header(ws, header_row=0, header_end=0, verbose=False):
    """
    :param header_end:
    :param ws: REQUIRED worksheet data
    :type ws: iterable
    :param header_row: starting row of data default 1
    :type header_row: int
    :return: dict
    :rtype dict: `outcolindex`
    """
    header_end = header_end if header_end >= header_row else header_row
    colindex = {u"{}".format(k).lower(): [] for k in ws[header_row]}
    for idx, val in enumerate(ws[header_row]):
        colindex[u"{}".format(val).lower()].append(idx)

    if verbose:
        print(colindex)

    return colindex


def rstrip_list(iterable, value):
    """
    Remove all instances of given value from the end of a list. Works like unicode().rstrip()
    :param iterable: iterable
    :param value: value to strip
    :return: list

    >>> rstrip_list([1,2,3,4,None,6,None,None,None], None)
    [1, 2, 3, 4, None, 6]
    >>> rstrip_list([1,2,3,4,5,5,5,5,5], 5)
    [1, 2, 3, 4]
    """
    i = iterable[::-1]
    if len(i) > 1:
        for idx, x in enumerate(i):
            while i[0] == value:
                i.remove(value)
    return i[::-1]


def lstrip_list(iterable, value):
    """
    Remove all instances of given value from the end of a list. Works like unicode().rstrip()
    :param iterable: iterable
    :param value: value to strip
    :return: list

    >>> lstrip_list([1,2,3,4,None,6,None,None,None], None)
    [1, 2, 3, 4, None, 6]
    >>> lstrip_list([1,2,3,4,5,5,5,5,5], 1)
    [1, 2, 3, 4]
    """
    i = iterable
    if len(i) > 1:
        for idx, x in enumerate(i):
            while i[0] == value:
                i.remove(value)
    return i


def explode_number(number):
    s = u"%s" % round(float(number), 2) if isnumber(number) else None
    if not s:
        raise TypeError('a number value is required')
    hund = None
    tenth = None
    whole = None
    if isnumber(number, 'float'):
        whl, dec = s.split('.')
        hund = int(dec[-1]) if len(dec) == 2 else 0
        tenth = int(s[-2]) if len(dec) == 2 else int(s[-1])
        whole = int(whl)
    elif isnumber(number, 'int'):
        hund = 0
        tenth = 0
        whole = int(number)

    return whole, tenth, hund


def simple_round_retail(price):
    """
    Round prices to our standard structure.
    1.09 -> 1.15
    1.05 -> .99
    1.00 -> .99
    1.11 -> 1.15
    1.16 -> 1.19
    1.20 -> 1.19
    1.92 -> 1.95
    1.96 -> 1.99
    :param price:
    :return:
    """
    whole, tenth, hund = explode_number(price)

    def __zero_x(w, t, h):
        if h < 9:
            if w > 0:
                w -= 1
                t = 9
                h = 9
            else:
                t = 1
                h = 5
        else:
            t = 1
            h = 5
        return w, t, h

    if tenth == 0:
        whole, tenth, hund = __zero_x(whole, tenth, hund)
        return float("{}.{}{}".format(whole, tenth, hund))

    elif hund not in [9, 5]:
        if hund < 5:
            if tenth == 1:
                tenth -= 1
                hund = 9
                whole, tenth, hund = __zero_x(whole, tenth, hund)
                return float("{}.{}{}".format(whole, tenth, hund))

            elif 5 < tenth < 9:
                tenth -= 1
                hund = 9

            else:
                hund = 5

            return float("{}.{}{}".format(whole, tenth, hund))

        if hund > 5:
            hund = 9
            return float("{}.{}{}".format(whole, tenth, hund))

    else:
        return float("{}.{}{}".format(whole, tenth, hund))


def yesno(text, default=True):
    """
    Parse a user input into true or false based on yes/no questions
    :param text:
    :param default:
    :return: bool
    """
    yesre = re.compile(r'^((?P<yes>Y(ES)?)|(?P<no>NO?))', re.IGNORECASE)
    yesnomatch = yesre.match(text)
    yes = default
    if yesnomatch or not text:
        yes = default
        if yesnomatch:
            yes = True if yesnomatch.group('yes') else False
            return yes
        if yes:
            return yes

    return yes


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def camel_to_snake_case(s):
    regex = r"([a-z]+)([A-Z]+)"
    return re.sub(regex, r"\1_\2", s).lower()


def string_to_snake(string: str) -> str:
    """
    Converts a string to lower case snake case.
    """
    return string.lower().replace(" ", "_")
