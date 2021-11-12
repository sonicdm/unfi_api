# permission error retry decorator
from openpyxl.utils import get_column_letter
from unfi_api.utils.string import  isnumber

# openpyxl methods
def size_cols(ws):
    for col in ws.columns:
        max_length = 0
        column = col[0].column  # Get the column name
        if isnumber(column):
            column = get_column_letter(column)
        for cell in col:
            try:  # Necessary to avoid error on empty cells
                if len(cell.value) > max_length:
                    max_length = len(cell.value)
            except TypeError:
                pass
        adjusted_width = (max_length + 1) * 1
        ws.column_dimensions[column].width = adjusted_width