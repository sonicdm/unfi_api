from __future__ import print_function

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox as mb

except ImportError:
    import Tkinter as tk
    from Tkinter import ttk
    import tkMessageBox as mb

from widgets import Heading, ButtonFrame, NavButtons
from utils import write_json, run_brdata
from settings import input_temp_file

PAGE_HEADING = u"UNFI Invoice Master."


class InventoryPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.container = ttk.Frame(self)
        self.controller = controller
        heading = Heading(self.container, controller, PAGE_HEADING)
        heading.pack()
        batch_field = ttk.Frame(self.container)
        batchcmd = self.register(self.batch_set)
        batch_label = ttk.Label(batch_field, text="Inventory Batch Number: ", width=24)
        batch_entry = ttk.Entry(batch_field, validate="key", validatecommand=(batchcmd, "%P"))
        batch_label.pack(side=tk.LEFT)
        batch_entry.pack(side=tk.RIGHT, expand=1)
        batch_field.pack()
        self.brdata_run = False
        self.brdframe = ButtonFrame(self.container, self, text="Click to run BRData report", command=self._run_brdata)
        self.brdframe.pack()
        self.nav_buttons = NavButtons(self,
                                      b1config={'command': lambda: controller.show_frame('StartPage')},
                                      b2config={},
                                      fill='x')
        self.container.pack(fill='both', expand=True)
        self.nav_buttons.pack(expand=True, fill='x')

    def batch_set(self, number):
        print("Batch Set ", number)
        if not number:
            return True
        try:
            self.controller.user_input['BATCH'] = int(number)
            return True
        except ValueError:
            mb.showerror("Invalid Batch Input", "You must use a number for your batch.")
            return False

    def _run_brdata(self):
        print("Ran BRdata")
        self.brdframe.button['state'] = 'disabled'
        run_brdata(self.controller.user_input['BATCH'])
        self.brdframe.destroy()
        self.next_step()

    def next_step(self):
        write_json(input_temp_file, self.controller.user_input)
