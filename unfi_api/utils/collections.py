from collections import Counter, OrderedDict
from typing import List, Any, Dict


def find_most_common_member(l):
    counts = Counter(l).most_common(1)
    if len(counts) > 0:
        return counts[0][0]


def sort_dict(d):
    od = OrderedDict((k, v) for k, v in sorted(d.items()))
    return od


def is_cur_col(key, cur_cols):
    cur_cols = set(["%s".lower() % x for x in cur_cols])
    key = u"%s" % key
    return len(set(key.lower().split(' ')).intersection(cur_cols)) > 0


def rstrip_list(iterable, value):
    """
    Remove all instances of given value from the end of a list. Works like str().rstrip()
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
    Remove all instances of given value from the end of a list. Works like str().rstrip()
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


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def table_to_dicts(table:List[Any], header_row:int=0, verbose:bool=False) -> List[Dict]:
    """
    Convert a table to a dict
    :param table:
    :return:
    """
    colindex = {val: idx for idx, val in enumerate(table[header_row])}
    return [dict(zip(colindex.keys(), row)) for row in table[header_row + 1:]]


def normalize_dict(d: dict) -> str:
    new_data = dict()
    for key, value in d.items():
        if not isinstance(value, dict):
            new_data[key] = value
        else:
            for k, v in value.items():
                new_data[key + "_" + k] = v

    return new_data