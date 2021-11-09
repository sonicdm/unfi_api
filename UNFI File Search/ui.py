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
        # label = tk.Label(self, text="Welcome to UNFI File Search", font=("Arial", 20))
        # label.pack(pady=10, padx=10)
        # self.search_button = ttk.Button(self, text="Search For Products", command=self.search_button_clicked)
        # self.search_button.pack(pady=10, padx=10)
        # canvas = tk.Canvas(
        #     self.container.master,
        #     bg = "#ffffff",
        #     height = 600,
        #     width = 600,
        #     bd = 0,
        #     highlightthickness = 0,
        #     relief = "ridge")
        # canvas.place(x = 0, y = 0)

        username_entry_img = tk.PhotoImage(file = os.path.join(ASSETS_DIR, f"img_textBox0.png"))
        username_entry_bg = self.container.canvas.create_image(
            300.0, 310.0,
            image = username_entry_img)

        self.username_entry = tk.Entry(
            bd = 0,
            bg = "#969e92",
            highlightthickness = 0)

        self.username_entry.place(
            x = 191.0, y = 293,
            width = 218.0,
            height = 32)

        password_entry_img = tk.PhotoImage(file =  os.path.join(ASSETS_DIR, f"img_textBox1.png"))
        password_entry_bg = self.container.canvas.create_image(
            300.0, 380.0,
            image = password_entry_img)

        self.password_entry = tk.Entry(
            bd = 0,
            bg = "#969e92",
            show="*",
            highlightthickness = 0,)

        self.password_entry.place(
            x = 191.0, y = 363,
            width = 218.0,
            height = 32)

        self.save_login = tk.IntVar(value=1)
        #unchecked
        img1 = tk.PhotoImage(file =  os.path.join(ASSETS_DIR, f"img1.png"))
        #checked
        img0 = tk.PhotoImage(file =  os.path.join(ASSETS_DIR, f"img0.png"))
        save_login_check = tk.Checkbutton(
            image = img1,
            selectimage=img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.save_login_checked,
            relief = "flat",
            variable = self.save_login)

        save_login_check.place(
            x = 215, y = 409,
            width = 21,
            height = 21)


        # b0 = Button(
        #     image = img0,
        #     borderwidth = 0,
        #     highlightthickness = 0,
        #     command = btn_clicked,
        #     relief = "flat")

        # b0.place(
        #     x = 218, y = 409,
        #     width = 20,
        #     height = 21)



        background_img = tk.PhotoImage(file =  os.path.join(ASSETS_DIR, f"background.png"))
        background = self.container.canvas.create_image(
            286.0, 263.0,
            image=background_img)

        img2 = tk.PhotoImage(file =  os.path.join(ASSETS_DIR, f"img2.png"))
        b2 = tk.Button(
            image = img2,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.search_button_clicked,
            relief = "flat")

        b2.place(
            x = 240, y = 465,
            width = 112,
            height = 40)
        

    def search_button_clicked(self):
        self.controller.show_view("search")
        print(self.username_entry.get()), print(self.password_entry.get())
    
    def save_login_checked(self):
        print(self.save_login.get())



class SearchPage(TkFrame):
    name: str = "search"
    title: str = "Product Search"
    def __init__(self, view: View, container: TkContainer, controller: 'SearchController', model=None):
        self.controller = controller
        self.container = container
        super().__init__(view, container, controller)
        label = tk.Label(self, text="Search", font=("Arial", 20))
        label.pack(pady=10, padx=10)
        # search entry box. multi line
        self.search_variable = tk.StringVar(container)
        self.search_entry = ScrolledText(self, height=10, width=50, wrap=tk.WORD)
        self.search_entry.pack()
        self.search_button = ttk.Button(self, text="Search", command=self.do_search)
        self.search_button.pack(pady=10, padx=10)
        self.search_entry.bind("<Return>", self.do_search)
        self.search_entry.bind("<KP_Enter>", self.do_search)
        self.next_button = ttk.Button(self, text="Next", command=self.next_button_clicked)
        self.next_button.pack(pady=10, padx=10, anchor=tk.W)
        self.next_button.config(state=tk.DISABLED)
        self.home_button = ttk.Button(self, text="Home", command=self.controller.show_main_view)
        self.home_button.pack(pady=10, padx=10, anchor=tk.E)

    
    def do_search(self, x=None):
        # do search
        query = self.search_entry.get("1.0", tk.END)
        self.search_variable.set(query)
        self.search_button.config(state=tk.DISABLED)    
        messagebox.showinfo("Search", "Searching for: " + query)
        if "poop" in query:
            self.next_button.config(state=tk.NORMAL)
        else:
            retry = messagebox.askretrycancel("Search", "No results found.. enter new query?")
            if  retry:
                self.search_entry.delete("1.0", tk.END)
                self.search_button.config(state=tk.NORMAL)
            else:
                self.controller.show_main_view()
            self.search_entry.delete("1.0", tk.END)
        
        # self.next_button.config(state=tk.NORMAL)

    def next_button_clicked(self):
        self.controller.show_view("download")

        # result = self.controller.search(query)

class DownloadPage(TkFrame):
    name: str = "download"
    def __init__(self, view, container, controller, model=None):
        super().__init__(view, container, controller)
        label = tk.Label(self, text="Download", font=("Arial", 20))
        label.pack(pady=10, padx=10)
        # progress bar to show product download progress
        # label progress bar as Download Progress %

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()

    

class SavePage(TkFrame):
    def __init__(self, parent, controller, model):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Save", font=("Arial", 20))
        label.pack(pady=10, padx=10)
        # filename entry box defaults to "F:\POS\unfi\query.xlsx"
        self.filename_variable = tk.StringVar()
        self.filename_variable.set(default_save_path)
        self.filename_entry = tk.Entry(self, width=50, textvariable=self.filename_variable)
        self.filename_entry.pack()





