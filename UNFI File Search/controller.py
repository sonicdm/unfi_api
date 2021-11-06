from typing import TYPE_CHECKING, Dict, List, Union
import tkinter as tk

if TYPE_CHECKING:
    from model import TkModel
    from view import View
    from container import TkContainer


class Controller:
    def __init__(self, title, container: TkContainer, model: TkModel=None):
        self.title = title
        self.model: TkModel = model(self)
        self.container: TkContainer = container(self, title)
        self.home_frame: str = None
        self.models: dict[str, TkModel] = {}
        self.ready = False

    def register_views(self, frames: List[View]) -> None:
        self.container.setup(frames)
        self.setup = True

    def show_view(self, name: str) -> None:
        model = self.container.show_view(name)
        self.container.show_view(name, model)

    def register_view(self, view: View) -> None:
        if not view.model:
            view.model = self.model
        self.container.register_view(view)
        self.ready = True

    def register_main_view(self, view: View) -> None:
        self.container.register_main_view(view)

    def destroy_view(self):
        self.container.destroy()

    def get_tk_variable(self, name: str, model_name: str = None) -> tk.Variable:
        if model_name in self.models:
            return self.models[model_name].get_tk_variable(name)
        return self.model.get_tk_variable(name)

    def store_tk_variable(self, name: str, value: str, model_name: str = None) -> None:
        if model_name in self.models:
            self.models[model_name].store_tk_variable(name, value)
        else:
            self.model.store_tk_variable(name, value)

    def get_variable_value(self, name: str, model_name: str = None) -> str:
        if model_name in self.models:
            return self.models[model_name].get_variable_value(name)
        return self.model.get_variable_value(name)

    def set_variable_value(self, name: str, value: str, model_name: str = None) -> None:
        if model_name in self.models:
            self.models[model_name].set_variable_value(name, value)
        else:
            self.model.set_variable_value(name, value)

    def run(self) -> None:
        if not self.ready:
            raise Exception("Controller not setup and ready to launch")
        
        self.container.run()
