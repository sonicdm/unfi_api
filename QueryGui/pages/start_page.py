import os

try:
    import tkinter as tk
    from tkinter import ttk, IntVar, BooleanVar, StringVar
    from tkinter import messagebox as mb
    from tkinter import filedialog as fd

except ImportError:
    import Tkinter as tk
    from Tkinter import ttk, IntVar, BooleanVar, StringVar
    import tkMessageBox as mb
    import tkFileDialog as fd
from tkcalendar import DateEntry
from datetime import datetime

# local imports
from utils import write_json, get_input, run_brdata
from widgets import SUBTITLE_FONT, LARGE_FONT, NavButtons
from settings import input_temp_file, base_folder

folder_format = u"%Y-%m-%d"
PAGE_HEADING = u"UNFI Invoice Master"
TODAY = datetime.today()


class StartPage(ttk.Frame):
    """
    First page of input:
    Fill out information and run the brdata report.
    """

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        # configure parent frame and register hooks
        self.bind_all('<<DateEntrySelected>>', self.date_clicked)
        self.container = ttk.Frame(self)

        # init instance vars
        self.file_set = False
        self.date = datetime.today()
        self.controller.user_input['DATE'] = "%s" % self.date
        self.filename = os.path.join(base_folder, TODAY.strftime(folder_format), u'invalue.csv')

        # Display the page headings
        headframe = tk.Frame(self.container)
        heading = ttk.Label(headframe, text=PAGE_HEADING, font=LARGE_FONT)
        heading.pack()
        headframe.grid(row=0, column=0, columnspan=3)

        # Create a calendar widget
        date_field = ttk.Frame(self.container)
        #         datefunc = date_field.register(self.set_date)
        #         self.bind('<Button-1>', datefunc)
        self.calendar = DateEntry(date_field, width=10)
        date_label = ttk.Label(date_field, text="Select the recieving date:", )
        date_label.grid(row=0, column=0, padx=10)
        self.calendar.grid(row=0, column=1, columnspan=2)
        date_field.grid(row=1, column=0, columnspan=3, sticky='n')

        # Inventory Checkbox

        self.run_brdata_report = True
        self.inventory_from_file = False
        self.run_inventory_report = True
        self.run_inventory = BooleanVar(value=True)
        self.run_report_var = IntVar(value=1)

        self.report_options_frame = ttk.Frame(self.container)
        report_heading = ttk.Label(self.report_options_frame, text="Inventory Report Options", font=SUBTITLE_FONT)
        report_heading.pack()
        self.report_options_frame.grid(row=2, columnspan=3, sticky='n')

        self.run_inventory_frame = ttk.Frame(self.container)
        self.inventory_box = ttk.Checkbutton(
            self.run_inventory_frame,
            variable=self.run_inventory,
            text="Run Inventory Report?",
            command=lambda: self.run_report_set(3)
        )
        self.inventory_box.pack(side="left")
        self.run_inventory_frame.grid(row=4)
        self.run_report_box = ttk.Radiobutton(self.container, variable=self.run_report_var, text="Pull from BRdata",
                                              value=1, command=lambda: self.run_report_set(1))
        self.run_report_box.grid(row=5, column=2, sticky='w')
        self.report_file_box = ttk.Radiobutton(self.container, variable=self.run_report_var, text="Choose from file",
                                               value=2, command=lambda: self.run_report_set(2))
        self.report_file_box.grid(row=5, column=0, sticky='w')

        # File selection area. Set default value to the selected date + base_path + invalue.csv
        self.fileframe = tk.Frame(self.container)
        self.file_path = self.default_file()
        self.file_var = StringVar(self.fileframe, value=self.filename)
        self.select_file_entry = ttk.Entry(
            self.fileframe,
            validate="key",
            validatecommand=(lambda: self.report_file_set, "%P"),
            textvariable=self.file_var,
            width=75,
        )
        self.select_file_entry.pack(side="left")

        # Browse Button
        self.browse_button = ttk.Button(self.fileframe, text=u"Browse", command=self.choose_file)
        self.browse_button.pack(side='right')

        # Place file selection frame
        self.fileframe.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky='w')

        self.container.pack(fill='both', expand=True)
        b2callback = {'command': lambda: self.next_step()}
        b1callback = {'command': lambda: self.controller.show_frame('WelcomePage')}
        self.nav_buttons = NavButtons(self, b1config=b1callback, b2config=b2callback)
        self.nav_buttons.pack(expand=True, fill='x', side='bottom')

    def run_report_set(self, option):
        self.run_inventory_report = self.run_report_var.get()
        if option == 1:
            self.run_inventory_report = True
            self.inventory_from_file = False
            self.run_brdata_report = True
            self.controller.user_input['run_brdata'] = True

        if option == 2:
            self.run_inventory_report = True
            self.run_brdata_report = False
            self.inventory_from_file = True
            self.controller.user_input['run_brdata'] = False

        if option == 3:
            self.run_inventory_report = self.run_inventory.get()
            if not self.run_inventory_report:
                self.report_file_box['state'] = 'disabled'
                self.select_file_entry['state'] = 'disabled'
                self.run_report_box['state'] = 'disabled'
                self.browse_button['state'] = 'disabled'
            else:
                self.report_file_box['state'] = 'active'
                self.select_file_entry['state'] = 'active'
                self.run_report_box['state'] = 'active'
                self.browse_button['state'] = 'active'

    def report_file_set(self, filepath):
        if os.path.exists(filepath):
            self.controller.user_input['inventory_file'] = self.file_var.get()
            self.file_var.set(filepath)

    def _update_values(self, field=None):
        if field == 'date':
            self.date = self.calendar.get_date()
            self.controller.user_input['date'] = self.date.strftime(folder_format)

    def date_clicked(self, event):
        """
        Catch clicks on the date selection widget and set the report date.

        :param event:
        :return:
        """
        print("set date", event.widget.get_date())
        self.date = event.widget.get_date()
        self.controller.user_input['date'] = self.date.strftime(folder_format)
        # TODO: figure out why this wont set the entry field variable. (Daddy issues maybe?)
        if not self.file_set:
            self.filename = self.default_file()
            self.choose_file(self.filename)
        print("set date", event.widget.get_date(), self.filename, self.file_var.get())

    def next_step(self):
        self.controller.user_input['date'] = "%s" % self.date
        self.unbind_all('<<DateEntrySelected>>')
        if self.run_inventory_report:
            self.controller.show_frame('InventoryPage')
        else:
            self.controller.show_frame('UNFIPage')

    def choose_file(self, fromstr=None):
        if fromstr:
            self.file_var.set(fromstr)
            return True
        else:
            path = os.path.join(base_folder, self.date.strftime(folder_format))
            if not os.path.exists(path):
                path = base_folder

            self.controller.user_input['REPORT'] = fd.askopenfilename(
                initialdir=path,
                filetypes=(("CSV File", ".csv"),)
            )

            self.file_var.set(self.controller.user_input['REPORT'])
        self.file_set = True

    def default_file(self):
        return os.path.join(base_folder, self.date.strftime(folder_format), 'invalue.csv')


class ReportFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
