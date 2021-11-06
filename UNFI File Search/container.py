import tkinter as tk    
from tkinter import ttk
from typing import TYPE_CHECKING, Dict, List
from exceptions import ViewRequiredException
if TYPE_CHECKING:
    from controller import Controller
    from model import TkModel
    from view import View



class TkContainer(tk.Tk):
    def __init__(self, controller: Controller, title: str):
        super().__init__()
        self.controller = controller
        self.title(self.base_title)
        self.geometry("600x400")
        self.resizable(False, False)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.views: Dict[str, View] = {}
        self.current_view: View = None

    def show_view(self, view_name: str):
        if self.current_view:
            self.current_view.lower_view()
        else:
            self.current_view = self.get_view(view_name)
            self.current_view.raise_view()

    def get_view(self, name: str) -> View:
        return self.views[name]

    def get_model(self, name: str) -> TkModel:
        return self.controller.get_model(name)

    def register_view(self, view: View, controller: Controller= None) -> View:
        controller = controller if controller else self.controller
        view.init_view(self, self.controller)
        self.views[view.name] = view
        return view

    def register_main_view(self, view: View):
        self.main_view = self.register_view(view)

    def unregister_view(self, view_name: str):
        view = self.views.pop(view_name)
        view.destroy_view()

    def get_tk_variable(self, name: str):
        return self.controller.get_tk_variable(name)

    def setup(self, views:List[View]=[], main_view:View=None):
        if main_view:
            self.register_view = main_view
            self.main_view = self.get_view(main_view.name)
        if views:
            self.frames = {}
            for v in views:
                self.register_view(v)
            if "main" not in self.frames and not main_view:
                # default to first view
                self.main_view = self.get_view(views[0].name)
            
    def run(self):
        if not self.views:
            raise ViewRequiredException("No views registered")
        if not self.main_view:
            raise ViewRequiredException("No main view registered")
        self.main_view.raise_view()
        self.mainloop()

    def destroy(self) -> None:
        return self.destroy()

    def store_tk_variable(self, name: str, value: str):
        self.controller.store_tk_variable(name, value)