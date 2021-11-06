from __future__ import annotations
import tkinter as tk
from tkinter import Variable, ttk
from tkinter import messagebox
from typing import TYPE_CHECKING
from settings import default_save_path
from view import TkContainer
from model import TkModel
from controller import Controller
if TYPE_CHECKING:
    from unfi_product_search import SearchController




            
# three page ui for Search, Download Progress, Save/Run Again

class MainContainer(TkContainer):

    def __init__(self, controller:Controller, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.base_title = "UNFI API Client"




        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome to UNFI File Search", font=("Arial", 20))
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Search", command=lambda: controller.show_frame(SearchPage))
        button1.pack()
        button2 = ttk.Button(self, text="Download", command=lambda: controller.show_frame(DownloadPage))
        button2.pack()
        button3 = ttk.Button(self, text="Save", command=lambda: controller.show_frame(SavePage))
        button3.pack()


class SearchPage(tk.Frame):
    name: str = "search"
    title: str = "Product Search"
    def __init__(self, parent, controller: SearchController, model=None):
        self.controller = controller
        self.parent = parent
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Search", font=("Arial", 20))
        label.pack(pady=10, padx=10)
        # search entry box. multi line
        self.search_variable = tk.StringVar()
        self.search_entry = tk.Text(self, height=5, width=50, textvariable=self.search_variable)
        self.search_entry.pack()
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_view(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Search", command=lambda: self.do_search)
        button2.pack()
        button3 = ttk.Button(self, text="Save", command=lambda: controller.show_view(SavePage))
        button3.pack()
    
    def do_search(self, x=None):
        # do search
        result = self.controller.search(self.search_variable.get)

class DownloadPage(tk.Frame):
    name: str = "download"
    def __init__(self, parent, controller, model):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Download", font=("Arial", 20))
        label.pack(pady=10, padx=10)
        # progress bar to show product download progress
        # label progress bar as Download Progress %

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()


        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Search", command=lambda: controller.show_frame(SearchPage))
        button2.pack()
        button3 = ttk.Button(self, text="Save", command=lambda: controller.show_frame(SavePage))
        button3.pack()
    

class SavePage(tk.Frame):
    def __init__(self, parent, controller, model):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Save", font=("Arial", 20))
        label.pack(pady=10, padx=10)
        # filename entry box defaults to "F:\POS\unfi\query.xlsx"
        self.filename_variable = tk.StringVar()
        self.filename_variable.set(default_save_path)
        self.filename_entry = tk.Entry(self, width=50, textvariable=self.filename_variable)
        self.filename_entry.pack()

        # run again button to run again with new query
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = ttk.Button(self, text="Search", command=lambda: controller.show_frame(SearchPage))
        button2.pack()
        button3 = ttk.Button(self, text="Download", command=lambda: controller.show_frame(DownloadPage))
        button3.pack()





