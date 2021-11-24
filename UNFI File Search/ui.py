from __future__ import annotations
import os
import tkinter as tk
from tkinter import Variable, ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from typing import TYPE_CHECKING
from settings import default_save_path
from container import TkContainer
from controller import Controller
from frame import TkFrame
from view import View
if TYPE_CHECKING:
    from unfi_product_search import SearchController


ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")


            
# three page ui for Search, Download Progress, Save/Run Again

class MainContainer(TkContainer):

    def __init__(self, controller:Controller, *args, **kwargs):
        self.base_title = "UNFI API Client"
        super().__init__(controller, self.base_title, *args, **kwargs)




        
class StartPage(TkFrame):
    def __init__(self, view: View, container:TkContainer, controller):
        super().__init__(view, container, controller)

    
    def create_widgets(self):
        ...
        

    def search_button_clicked(self):
        self.controller.show_view("search")
        print(self.username_entry.get()), print(self.password_entry.get())
    
    def save_login_checked(self):
        print(self.save_login.get())





def make_and_grid_container(master, row, column, rowspan=1, columnspan=1, sticky="")-> tk.Frame:
    frame = tk.Frame(master)
    frame.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)