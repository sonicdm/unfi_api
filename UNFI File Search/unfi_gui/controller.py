from threading import Thread
from typing import TYPE_CHECKING, Dict, List, Union
import tkinter as tk
import tkinter.ttk as ttk
from unfi_api.utils.threading import stop_job, stop_all_jobs

if TYPE_CHECKING:
    from model import TkModel
    from view import View
    from container import TkContainer


class Controller:
    def __init__(self, title, container: "TkContainer", model: "TkModel" = None):
        self.title = title
        self.model: "TkModel" = model(self)
        self.container: "TkContainer" = container(self, title)
        self.home_frame: str = None
        self.models: dict[str, TkModel] = {}
        self.ready: bool = False
        self.jobs = []
        self.cancel = []
        self.cancel_all = False
        self.thread_pool: Dict[str, Thread] = {}
    
    def register_views(self, frames: List["View"]) -> None:
        self.container.setup(frames)
        self.setup = True

    def show_view(self, name: str, model_name: str = None) -> None:
        self.container.show_view(name)

    def show_main_view(self) -> None:
        self.container.show_main_view()

    def register_view(self, view: "View") -> None:
        if not view.model:
            view.model = self.model
        self.container.register_view(view)
        self.ready = True

    def register_main_view(self, view: "View") -> None:
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

    def quit(self) -> None:
        self.container.destroy()
        
    
    def setup(self) -> None:
        ...
    
    def add_job_id(self, job_id: Union[str, int]) -> None:
        self.jobs.append(job_id)
    
    def stop_job(self, job_id: Union[str, int]) -> None:
        if job_id in self.jobs:
            stop_job(job_id)

    def stop_all_jobs(self) -> None:
        for job_id in self.jobs:
            stop_job(job_id)
    
    def stop_cancelled_jobs(self) -> None:
        for job_id in self.cancel:
            stop_job(job_id)
            self.cancel.remove(job_id)
    
    def cancel_job(self, job_id: Union[str, int]) -> None:
        self.cancel.append(job_id)
    
    def cancel_all_jobs(self) -> None:
        self.cancel_all = True
        self.stop_all_jobs()
    
    def stop_thread(self, thread_id: Union[str, int]) -> None:
        if thread_id in self.thread_pool:
            self.thread_pool[thread_id].join()
            del self.thread_pool[thread_id]