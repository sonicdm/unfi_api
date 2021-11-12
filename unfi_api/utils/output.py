
from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from openpyxl.worksheet.worksheet import Worksheet


def auto_size_worksheet_columns(ws: Worksheet, padding: int=0) -> None:
    """
    Automatically resize all columns in a worksheet
    """
    dims = {}
    for row in ws.rows:
        for cell in row:
            if cell.value:
                dims[cell.column] = max((dims.get(cell.column, 0), len(str(cell.value))))    
    for col, value in dims.items():
        ws.column_dimensions[col].width = value
    
