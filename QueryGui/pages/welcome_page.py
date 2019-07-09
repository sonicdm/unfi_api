from __future__ import print_function

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox as mb

except ImportError:
    import Tkinter as tk
    from Tkinter import ttk
    import tkMessageBox as mb

from widgets import CONTENT_FONT, LARGE_FONT, NavButtons

PAGE_HEADING = u"UNFI Invoice Master"

WELCOME_TEXT = (
    u"This will walk you through the process of downloading\n"
    u"and processing UNFI invoices.\n\n"
    u"Click Continue to begin."
)


class WelcomePage(ttk.Frame):
    def __init__(self, parent, controller):
        # Class Variables

        self.sToken = ""
        self.sQuery = ""

        # Build frame
        ttk.Frame.__init__(self, parent)
        # self.pack_propagate(0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.container = ttk.Frame(self)
        self.tksTokenVar = tk.StringVar(self.container, name="token")
        heading = ttk.Label(
            self.container,
            text="UNFI PRODUCT QUERY",
            font=LARGE_FONT,
            justify='center'
        )
        heading.grid(sticky='n')
        query_label = ttk.Label(
            self.container,
            text="Enter in your search terms:",
            font=CONTENT_FONT,
            justify='center'
        )
        query_label.grid(sticky='nw')

        self.query_box = ttk.Entry(
            self.container,
            validate="key",
            validatecommand=(lambda: self.set_token, "%P"),
            textvariable=self.tksTokenVar,
            width=75,
        )
        self.query_box.grid(sticky="ne")

        query_button = tk.Button(
            self.container,
            text=u"Search",
            command=self.query_button
        )
        query_button.grid(sticky="ne")
        self.container.grid(pady=10, padx=10, sticky='n')
        nav_buttons = NavButtons(
            self,
            b1config={'command': lambda: quit(0), 'text': "Quit"},
            b2config={'command': lambda: controller.show_frame('StartPage'), 'text': 'Continue'},
            expand=True,
        )
        nav_buttons.grid(sticky='s')

    def set_token(self, text):
        self.sToken = text

    def query_button(self):
        self.sQuery = self.query_box.get()
        self.run_query(self.sQuery)

    def run_query(self, query):
        pass

    def ask_token(self, wh):
        pass
