from __future__ import annotations

import os
from re import search
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Listbox, messagebox
from tkinter.scrolledtext import ScrolledText
from typing import Callable, Dict, List, Union

from unfi_api import UnfiAPI, UnfiApiClient
from unfi_api.product.product import UNFIProduct
from unfi_api.search.result import ProductResult, Result, Results
from unfi_api.utils.collections import divide_chunks, lower_case_keys

from container import TkContainer
from controller import Controller
from exceptions import UnfiApiClientNotSetException
from frame import TkFrame
from model import TkModel
from settings import (
    search_chunk_size,
    auto_download,
    default_save_path,
    auto_login,
    auto_save,
    username,
    password,
    save_settings,
)
from view import View


class SearchPage(TkFrame):
    name: str = "search"
    title: str = "Product Search"

    def __init__(
        self,
        view: View,
        container: TkContainer,
        controller: SearchController,
        model=None,
    ):
        super().__init__(view, container, controller)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.controller: Controller = controller
        self.controller_model: TkModel = controller.model
        self.container: TkContainer = container
        self.view: View = view
        self.model: TkModel = view.model
        self.view_controller: Controller = view.controller
        label = tk.Label(self, text="Product Search", font=("Arial", 20))
        label.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # container for the search entry box and results listbox columns
        self.column_container = tk.Frame(self)
        self.column_container.grid(row=1, column=0, sticky="nsew", columnspan=2)
        self.column_container.columnconfigure(0, weight=1)
        self.column_container.rowconfigure(0, weight=1)

        # options frame
        self.options_frame = tk.Frame(self)
        self.options_frame.grid(row=2, column=0, sticky="nsew")
        
        # progress bar frame
        self.progress_bar_frame = tk.Frame(self)
        self.progress_bar_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")
        # progress bars
        self.search_progress_bar = ttk.Progressbar(
            self.progress_bar_frame,
            orient=tk.HORIZONTAL,
            length=100,
            mode="determinate",
        )
        self.download_progress_bar = ttk.Progressbar(
            self.progress_bar_frame,
            orient=tk.HORIZONTAL,
            length=100,
            mode="determinate",
        )
        
        # instance widgets
        self.search_entry: ScrolledText = None
        self.results_listbox: Listbox = None
        # tkinter variables
        self.results_listbox_variable = tk.StringVar(
            container, value="Found Products: "
        )
        self.list_box_selected = tk.StringVar(container)
        self.search_variable = tk.StringVar(container)
        self.list_box_label = tk.StringVar(container)
        self.search_entry_label = tk.StringVar(container, value="Search: ")
        self.selected = []

        # options variables
        self.auto_download_variable = tk.BooleanVar(container)
        self.auto_login_variable = tk.BooleanVar(container)
        self.save_settings_variable = tk.BooleanVar(container)
        self.auto_save_variable = tk.BooleanVar(container)
        self.save_new_path_variable = tk.BooleanVar(container)
        self.save_path_variable = tk.StringVar(container)

        # register tkinter variables with controller
        self.controller.store_tk_variable("auto_download", self.auto_download_variable)
        self.controller.store_tk_variable("auto_login", self.auto_login_variable)
        self.controller.store_tk_variable("save_settings", self.save_settings_variable)
        self.controller.store_tk_variable("auto_save", self.auto_save_variable)
        self.controller.store_tk_variable("save_new_path", self.save_new_path_variable)
        self.controller.store_tk_variable("search_variable", self.search_variable)
        self.controller.store_tk_variable("save_path", self.save_path_variable)
        self.controller.store_tk_variable(
            "results_listbox_variable", self.results_listbox_variable
        )
        self.controller.store_tk_variable("list_box_selected", self.list_box_selected)

        self.listbox_map: Dict[str, UNFIProduct] = {}

        self.download_button = None

        self.create_widgets()

    

    ### listbox functions ###
    def create_listbox_column_widgets(self):
        list_box_container = tk.Frame(self.column_container)
        list_box_container.grid(row=0, column=1, sticky="nsew")
        list_box_container.grid_columnconfigure(0, weight=1)
        list_box_container.grid_rowconfigure(0, weight=1)
        list_box_label = tk.Label(
            list_box_container,
            textvariable=self.results_listbox_variable,
            font=("Arial", 15),
        )
        list_box_label.grid(row=0, column=0, columnspan=2, sticky="nsew")
        # multi select listbox with scrollbar.
        list_box = tk.Listbox(
            list_box_container, selectmode=tk.MULTIPLE, height=10, width=100
        )
        self.results_listbox = list_box
        list_box.grid(row=1, column=0, sticky="nsew")
        # enable download button if listbox has items
        list_box.bind(
            "<<ListboxSelect>>", lambda x: self.list_box_select(listbox=list_box)
        )
        scroll_bar = tk.Scrollbar(
            list_box_container, orient=tk.VERTICAL, command=list_box.yview
        )
        scroll_bar.grid(row=1, column=1, sticky="ns")
        list_box.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=list_box.yview)
        self.download_button = tk.Button(
            list_box_container, text="Download", command=self.do_download
        )
        select_buttons_frame = tk.Frame(list_box_container)
        select_all_button = tk.Button(
            select_buttons_frame,
            text="Select All",
            command=lambda: self.list_box_select_all(list_box),
        )
        select_none_button = tk.Button(
            select_buttons_frame,
            text="Select None",
            command=lambda: self.list_box_deselect_all(list_box),
        )
        select_all_button.grid(row=1, column=0, sticky="nsew")
        select_none_button.grid(row=1, column=1, sticky="nsew")
        select_buttons_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        remove_button = tk.Button(
            select_buttons_frame,
            text="Remove",
            command=lambda: self.list_box_delete_selection(list_box),
        )
        remove_all_button = tk.Button(
            select_buttons_frame,
            text="Remove All",
            command=lambda: self.list_box_delete_all(list_box),
        )
        remove_button.grid(row=1, column=2, sticky="nsew")
        remove_all_button.grid(row=1, column=3, sticky="nsew")

        # disable download button until a product is selected
        self.download_button.config(state=tk.DISABLED)
        self.download_button.grid(row=3, column=1, sticky="nsew")
        
    def list_box_select(self, listbox: tk.Listbox = None):
        self.download_button.config(state=tk.NORMAL)
        self.selected = [listbox.get(idx) for idx in listbox.curselection()]

    def list_box_deselect(self, listbox: tk.Listbox):
        self.selected = listbox.curselection()
        if len(self.selected) == 0:
            self.download_button.config(state=tk.DISABLED)

    def list_box_select_all(self, listbox: tk.Listbox):
        if self.results_listbox.size() > 0:
            self.download_button.config(state=tk.NORMAL)
        listbox.select_set(0, tk.END)

    def list_box_deselect_all(self, listbox: tk.Listbox):
        self.download_button.config(state=tk.DISABLED)
        listbox.select_clear(0, tk.END)

    def list_box_delete_all(self, listbox: tk.Listbox):
        self.download_button.config(state=tk.DISABLED)
        listbox.delete(0, tk.END)

    def list_box_delete_selection(self, listbox: tk.Listbox):
        for i in listbox.curselection():
            listbox.delete(i)
        if self.results_listbox.size() < 1:
            self.download_button.config(state=tk.DISABLED)

    ### search entry functions ###
    def create_search_entry_frame(self):
        # multi line text entry box with scrollbar and search button
        search_entry_container = tk.Frame(self.column_container)
        search_entry_container.grid(row=0, column=0, sticky="nsew")
        search_entry_container.grid_columnconfigure(0, weight=1)
        search_entry_container.grid_rowconfigure(0, weight=1)
        search_label = tk.Label(
            search_entry_container, textvariable=self.search_entry_label, font=("Arial", 15)
        )
        search_label.grid(row=0, column=0, sticky="nsew")
        self.search_entry = ScrolledText(
            search_entry_container,
            height=10,
            width=50,
            wrap=tk.WORD,
        )
        self.search_entry.grid(row=1, column=0, columnspan=2 ,sticky="")
        self.search_button = tk.Button(
            search_entry_container, text="Search", command=self.do_search
        )
        self.search_button.config(state=tk.DISABLED)
        self.search_button.grid(row=2, column=0, sticky="nsew")
        # auto download checkbox
        self.auto_download_checkbox = tk.Checkbutton(
            search_entry_container,
            text="Auto Download",
            variable=self.auto_download_variable,
        )
        self.auto_download_checkbox.grid(row=2, column=1, sticky="nsew")

        # enable/disable search button when search entry box gets input
        self.search_entry.bind(
            "<KeyRelease>", lambda x: self.search_entry_key_release()
        )

    def search_entry_key_release(self, event=None):
        # if entry is empty, disable search button
        value = self.search_entry.get("1.0", tk.END).strip()
        if not value:
            self.search_button.config(state=tk.DISABLED)
        else:
            self.search_button.config(state=tk.NORMAL)
            # self.search_variable.set(value)

    def save_settings(self):
        auto_download = self.auto_download_variable.get()
        auto_login = self.auto_login_variable.get()
        auto_save = self.auto_save_variable.get()
        if self.save_new_path_variable.get():
            save_path = self.save_path_variable.get()


    ### options frame functions ###
    def create_options_frame(self):
        options_frame_container = tk.Frame(self.options_frame)
        options_frame_container.grid(row=1, column=0, sticky="nsew")
        ## make checkbuttons for all options
        auto_save_checkbutton = tk.Checkbutton(
            options_frame_container,
            text="Auto Save",
            variable=self.auto_save_variable,
        )
        auto_save_checkbutton.grid(row=0, column=0, sticky="nsew")
        auto_login_checkbutton = tk.Checkbutton(
            options_frame_container,
            text="Auto Login",
            variable=self.auto_login_variable,
        )
        auto_login_checkbutton.grid(row=0, column=1, sticky="nsew")
        auto_download_checkbutton = tk.Checkbutton(
            options_frame_container,
            text="Auto Download",
            variable=self.auto_download_variable,
        )
        auto_download_checkbutton.grid(row=0, column=2, sticky="nsew")
        save_new_path_checkbutton = tk.Checkbutton(
            options_frame_container,
            text="Save to New Path",
            variable=self.save_new_path_variable,
        )
        save_new_path_checkbutton.grid(row=0, column=3, sticky="nsew")
        save_path_checkbutton = tk.Checkbutton(
            options_frame_container,
            text="Save to Path",
            variable=self.save_path_variable,
        )
        save_path_checkbutton.grid(row=0, column=4, sticky="nsew")

    def create_widgets(self):
        """
        make 2 columns. left side multi line text entry box. Right side listbox with search results.
        """
        # search query entry box. multi line. left column
        self.create_search_entry_frame()
        self.create_listbox_column_widgets()



    # action functions
    def do_search(self, x=None):
        # do search
        query = self.search_entry.get("1.0", tk.END)
        self.search_variable.set(query)
        self.search_button.config(state=tk.DISABLED)
        auto_download = self.auto_download_variable.get()
        messagebox.showinfo(
            "Search",
            "Searching for: " + query + "\nAuto Download: " + str(auto_download),
        )
        self.search_button.config(state=tk.NORMAL)

        if "poop" in query:
            # self.results_listbox_variable.set(['poop'])
            for q in query.split("\n"):
                if q.strip():
                    self.results_listbox.insert(tk.END, q)
            self.list_box_select_all(self.results_listbox)
        else:
            retry = messagebox.askretrycancel(
                "Search", "No results found.. enter new query?"
            )
            if retry:
                self.search_entry.delete("1.0", tk.END)
                self.search_button.config(state=tk.NORMAL)
            else:
                self.controller.show_main_view()
            self.search_entry.delete("1.0", tk.END)

        # self.next_button.config(state=tk.NORMAL)

    def do_download(self):
        # self.model.download()
        selection = self.results_listbox.curselection()
        messagebox.showinfo(
            "Download",
            "Downloading:\n"
            + "\n".join(
                [str(idx) + ": " + self.results_listbox.get(idx) for idx in selection]
            ),
        )

    def save_wb(self, end=False):
        pass


class SearchModel(TkModel):
    """
    usage:
    """

    client: UnfiApiClient = None

    def __init__(self, controller: Controller, client: UnfiApiClient = None):
        super().__init__(controller)
        if not self.get_client() and not client:
            raise UnfiApiClientNotSetException("Client not set")
        elif not self.client and client:
            self.client = client

        self.controller = controller
        self.products: List[UNFIProduct] = []
        self.results: Result = None

    @classmethod
    def set_client(cls, client: UnfiApiClient):
        cls.client = client

    @classmethod
    def get_client(cls) -> UnfiApiClient:
        return cls.client

    def download(self, filename: str, threaded: bool = True, callback: Callable = None):
        self.products.extend(
            self.results.download_products(
                self.client, threaded=threaded, callback=callback
            )
        )

    def add_product(self, product: UNFIProduct) -> None:
        self.products.append(product)

    def add_products(self, products: List[UNFIProduct]) -> None:
        self.products.extend(products)

    def add_results(self, results: Results) -> None:
        if not self.results:
            self.results = results
        else:
            self.results.extend_results(results)

    def add_result(self, result: Result) -> None:
        if not self.results:
            self.results = Results([result])
        else:
            self.results.append_result(result)

    def search(self, query: str, limit: int = None):
        result = self.client.search(query, limit)
        if isinstance(result, Result):
            self.add_result(result)
        elif isinstance(result, Results):
            self.add_results(result)

        if not self.results:
            self.results = Results([self.result])


class SearchController(Controller):
    def __init__(
        self, container: TkContainer, model: TkModel, search_model: SearchModel
    ):
        container = container
        self.search_model: SearchModel = search_model(self)
        super().__init__("unfi_api_search", container, model)

    def search(self, query: str, callback: Callable = None) -> Results:
        client = self.search_model.get_client()
        results = []
        for chunk in list(divide_chunks(query, search_chunk_size)):
            self.search_model.search(chunk)

    def download_products(
        self, result: Union[Results, Result], callback=None
    ) -> List[UNFIProduct]:
        return result.download_products(callback=callback)

    def save_workbook(self, products: List[UNFIProduct], callback=None):
        excel_dicts = [product.to_excel_dict() for product in products]
        dict_keys = set(sorted([key for d in excel_dicts for key in d.keys()]))
