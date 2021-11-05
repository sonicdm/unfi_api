from typing import Any, Dict
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

def create_workbook(tab_name=None) -> Workbook:
    wb = Workbook()
    ws = wb.active
    if tab_name:
        ws.title = tab_name
    return wb


def write_worksheet_rows(ws: Worksheet, excel_dict:Dict[str, Dict[str, Any]]) -> None:
    header_keys = [key for d in excel_dict.values() for key in d.keys()]
    header_keys = list(set(header_keys))
    header_keys.sort()
    rows = []
    for d in excel_dict.values():
        row = []
        for key in header_keys:
            row.append(d.get(key, ""))
        rows.append(row)

    ws.append(header_keys)
    for row in rows:
        ws.append(row)


def save_workbook(wb, filename) -> None:
    wb.save(filename)