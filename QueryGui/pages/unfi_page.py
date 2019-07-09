from QueryGui.tkCompat import *

import os

from tkcalendar import DateEntry
from datetime import datetime

# local imports
from utils import write_json, get_input, run_brdata
from widgets import SUBTITLE_FONT, LARGE_FONT, NavButtons
from settings import input_temp_file, base_folder

folder_format = u"%Y-%m-%d"
PAGE_HEADING = u"UNFI Invoice Master"
TODAY = datetime.today()


class UNFIPage(ttk.Frame):
    """
    First page of input:
    Fill out information and run the brdata report.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # configure parent frame and register hooks
        self.container = ttk.Frame(self)

        # Display the page headings
        headframe = tk.Frame(self.container)
        heading = ttk.Label(headframe, text=PAGE_HEADING, font=LARGE_FONT)
        heading.pack()
        headframe.pack(expand=True, fill='both', side='bottom')

        self.container.pack(side='top')
        b2callback = {'command': lambda: controller.show_frame('StartPage')}
        b1callback = {'command': lambda: quit, 'text': 'Quit'}
        self.nav_buttons = NavButtons(self, b1config=b1callback, b2config=b2callback)
        self.nav_buttons.pack(expand=True, fill='x', side='bottom')


class InvoiceSelect(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        # configure parent frame and register hooks
        self.container = ttk.Frame(self)
