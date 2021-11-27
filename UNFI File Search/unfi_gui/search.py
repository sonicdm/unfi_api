from __future__ import annotations

import os
import time
import tkinter as tk
import tkinter.ttk as ttk
from re import S, search
from tkinter import Listbox, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from typing import Callable, Dict, List, Union

from unfi_api import UnfiAPI, UnfiApiClient
from unfi_api.product.product import UNFIProduct, UNFIProducts
from unfi_api.search.result import ProductResult, Result, Results
from unfi_api.utils.collections import divide_chunks, lower_case_keys
from unfi_api.utils.string import divide_list_into_chunks_by_character_limit
from unfi_api.settings import config
from unfi_api.utils.threading import threader
from .container import TkContainer
from .controller import Controller
from .controllers.search import SearchController
from .exceptions import UnfiApiClientNotSetException
from .frame import TkFrame
from .model import TkModel
from .settings import (
    auto_download,
    auto_login,
    auto_save,
    default_save_path,
    password,
    save_settings,
    search_chunk_size,
    update_settings,
    username,
)
from .ui import QueryFrame, ProductListFrame, OptionsFrame
from .view import View
from .download import DownloadModel
from .models.search import SearchModel


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
        self.controller: SearchController = controller
        self.controller_model: TkModel = controller.model
        self.search_model: SearchModel = controller.search_model
        self.download_model: DownloadModel = controller.download_model
        self.container: TkContainer = container
        self.view: View = view
        self.model: TkModel = view.model
        self.view_controller: Controller = view.controller
        label = tk.Label(self, text="UNFI Product Search", font=("Arial", 20))
        label.grid(row=0, column=0, sticky="nsew")

        # instance widgets
        self.search_entry: ScrolledText = None
        self.results_listbox: Listbox = None
        self.progress_bar: ttk.Progressbar = None

        # tkinter variables
        self.results_listbox_variable = tk.StringVar(
            container, value="Found Products:"
        )
        self.list_box_selected = tk.StringVar(container)
        self.search_variable = tk.StringVar(container)
        self.list_box_label = tk.StringVar(container)
        self.search_entry_label = tk.StringVar(container, value="Search: ")
        self.selected = []
        self.progress_label_variable = tk.StringVar(container)

        # options variables
        self.auto_download_variable = tk.BooleanVar(container, value=auto_download)
        self.auto_login_variable = tk.BooleanVar(container, value=auto_login)
        self.auto_save_variable = tk.BooleanVar(container, value=auto_save)
        self.save_new_path_variable = tk.BooleanVar(container)
        # get parent folder of default_save_path
        self.save_path_variable = tk.StringVar(container, value=default_save_path)

        # register tkinter variables with controller
        self.controller.store_tk_variable("auto_download", self.auto_download_variable)
        self.controller.store_tk_variable("auto_login", self.auto_login_variable)
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
        
        ### create frames ###

        # container for the search entry box and results listbox columns
        self.column_container = tk.Frame(self)
        self.column_container.grid(
            row=1, column=0, sticky="", columnspan=2, padx=10, pady=10
        )
        # column container frames
        ### search entry frame ###
        self.search_frame: QueryFrame = QueryFrame(self, self.column_container)
        self.search_frame.grid(row=0, column=0, sticky="ns", pady=10)
        ### results listbox frame ###
        self.listbox_frame: ProductListFrame = ProductListFrame(self, self.column_container)
        self.listbox_frame.grid(row=0, column=1, sticky="ns", pady=10)

        # options frame
        self.options_frame: OptionsFrame = OptionsFrame(self, self)
        self.options_frame.grid(row=2, column=0, sticky="", pady=10)

        # progress bar frame
        self.progress_bar_frame = tk.Frame(self)
        self.progress_bar_frame.grid(row=3, column=0, sticky="", pady=10)
        self.cancel_button = tk.Button(self.progress_bar_frame, text="Cancel", command=controller.cancel_all_jobs)

        # action buttons frame
        self.save_exit_button: tk.Button = None
        self.save_button: tk.Button = None
        self.exit_button: tk.Button = None
        self.action_buttons_frame = tk.Frame(self)
        self.action_buttons_frame.grid(row=4, column=0, sticky="s", pady=10)

        self.create_widgets()

    ### progress frame functions ###
    def create_progress_frame_widgets(self):
        progress_frame_container = tk.Frame(self.progress_bar_frame)
        progress_frame_container.grid(row=1, column=0, sticky="")
        progress_frame_container.columnconfigure(0, weight=1)
        self.progress_label = tk.Label(
            progress_frame_container, textvariable=self.progress_label_variable
        )
        self.progress_label.grid(row=0, column=0, sticky="")

        self.progress_bar = ttk.Progressbar(
            progress_frame_container,
            orient=tk.HORIZONTAL,
            mode="determinate",
            length=800,
        )
        self.progress_bar.grid(row=1, column=0, columnspan=5, sticky="")
        
        self.cancel_button.grid(row=2, column=0, sticky="", pady=10)
        self.cancel_button.config(state=tk.DISABLED)
                                
    def create_action_buttons_frame_widgets(self):
        action_buttons_frame_container = tk.Frame(self.action_buttons_frame)
        action_buttons_frame_container.grid(row=1, column=0, sticky="e")
        # save button, exit button, save and exit button
        self.save_button = tk.Button(action_buttons_frame_container, text="Save",
                                     command=lambda: self.save_wb(end=False))
        self.save_button.grid(row=0, column=0, sticky="e")
        self.save_button.config(state=tk.DISABLED)
        self.save_exit_button = tk.Button(action_buttons_frame_container, text="Save and Exit",
                                          command=lambda: self.save_wb(end=True))
        self.save_exit_button.grid(row=0, column=1, sticky="e")
        self.save_exit_button.config(state=tk.DISABLED)
        self.exit_button = tk.Button(action_buttons_frame_container, text="Exit",
                                     command=lambda: self.controller.quit())
        self.exit_button.grid(row=0, column=2, sticky="e")

    def create_widgets(self):
        """
        make 2 columns. left side multi line text entry box. Right side listbox with search results.
        """
        # search query entry box. multi line. left column
        # self.create_search_entry_widgets()
        # self.create_listbox_column_widgets()
        self.create_progress_frame_widgets()
        self.create_action_buttons_frame_widgets

    # action functions
    def update_progress_bar(self, value: int, max_value: int, message=None):
        self.progress_bar.config(maximum=max_value)
        self.progress_bar.config(value=value)
        if message:
            self.progress_label_variable.set(message)
        self.progress_bar.update()

    def do_search(self, event=None, entry=None, search_button: tk.Button = None, listbox: tk.Listbox = None):
        job_id = 'search'
        
        def __search_callback(result, pb_value, pb_max, found_count):
            message = f"Searched {pb_value}/{pb_max} terms.\nFound {found_count} results."
            self.update_progress_bar(pb_value, pb_max, message)

        # do search
        if not listbox:
            listbox = self.listbox_frame.results_listbox
        if not entry:
            entry = self.search_frame.search_entry
        if not search_button:
            search_button = self.search_frame.search_button
        query = entry.get("1.0", tk.END)

        # update listbox
        listbox.delete(0, tk.END)
        self.search_variable.set(query)
        search_button.config(state=tk.DISABLED)
        auto_download = self.auto_download_variable.get()
        listbox_parent = listbox.master
        messagebox.showinfo(
            "Search",
            "Searching for: " + query + "\nAuto Download: " + str(auto_download),
        )
        query_split = list(filter(lambda x: str(x).strip() != "", query.split()))
        query_split = list(set(query_split))
        query_list = self.search_model.remove_already_searched_terms(query_split)
        duplicate_count = len(query_split) - len(query_list)
        if duplicate_count > 0:
            messagebox.showinfo("Duplicates Removed", f"Removed {duplicate_count} terms already searched.")
        if len(query_list) < 1:
            messagebox.showinfo("Search", "No new terms to search for.")
            return
        self.progress_label_variable.set(f"Searching for: {len(query_list)} terms...")
        if "poop" in query:
            results = []
        else:
            results = self.search_model.search(query_list, progress_callback=__search_callback, job_id=job_id)
        self.cancel_button.config(state=tk.NORMAL, command=lambda: self.controller.cancel_job(job_id))
        
        self.listbox_frame.list_box_delete_all(listbox=listbox)
        if len(results) < 1:
            retry = messagebox.showinfo(
                "Search", "No results found..."
            )
            search_button.config(state=tk.NORMAL)
            
        for result in self.search_model.results:
            list_val = result + " unfi product description"
            self.listbox_map[list_val] = result
            listbox.insert(tk.END, list_val)
            
        if self.auto_download_variable.get():
            self.do_download()

        # self.next_button.config(state=tk.NORMAL)

    def do_download(self, listbox=None, download_button: tk.Button = None, search_button: tk.Button = None):
        # self.model.download()
        job_id = 'download'
        if not listbox:
            listbox = self.listbox_frame.results_listbox
        if not download_button:
            download_button = self.listbox_frame.download_button
        if not search_button:
            search_button = self.search_frame.search_button
        search_button.config(state=tk.DISABLED)
        selection = listbox.curselection()
        selection_items = [listbox.get(i) for i in selection]
        messagebox.showinfo("Download", "Downloading:\n" + "\n".join(selection_items))
        downloaded = 0
        # run through items and update progress bar
        self.progress_bar.config(maximum=len(selection_items))
        self.progress_label_variable.set(
            f"Downloaded: {downloaded}/{len(selection_items)}"
        )
        model = self.download_model
        for i in selection_items:
            time.sleep(1)
            downloaded += 1
            self.update_progress_bar(downloaded, len(selection_items),
                                     f"Downloaded: {downloaded}/{len(selection_items)}")

        self.progress_label_variable.set(
            f"Downloading {len(selection_items)} products complete!"
        )

        if self.auto_save_variable.get():
            self.save_wb()
        search_button.config(state=tk.NORMAL)

    def save_wb(self, end=False):
        messagebox.showinfo("Save", f"Saved {self.save_path_variable.get()}")
        if end:
            open_ws = messagebox.askyesno("Save", "Saved and exiting. Open File?")
            if open_ws:
                os.system(f"start {self.save_path_variable.get()}")
            self.controller.quit()

    def save_settings(self):
        """
        auto_download,
        default_save_path,
        auto_login,
        auto_save,
        """
        new_settings = {}
        auto_download = self.auto_download_variable.get()
        auto_login = self.auto_login_variable.get()
        auto_save = self.auto_save_variable.get()
        if self.save_new_path_variable.get():
            save_path = self.save_path_variable.get()
            new_settings["default_save_path"] = save_path
        new_settings["auto_download"] = auto_download
        new_settings["auto_login"] = auto_login
        new_settings["auto_save"] = auto_save
        update_settings(new_settings)
        save_settings()
        messagebox.showinfo("Settings Saved", "Settings saved")









