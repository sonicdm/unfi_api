from __future__ import annotations
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from typing import Callable, Dict, List, Union
from view import TkContainer, View
from model import TkModel
from controller import Controller
from ui import StartPage, MainContainer
from unfi_api.client import UnfiApiClient
from unfi_api.api import UnfiAPI
from unfi_api.product import UNFIProduct
from unfi_api.search.result import Result, Results
from excel import create_workbook, save_workbook, write_worksheet_rows
from settings import search_chunk_size
from unfi_api.utils.collections import divide_chunks


def main():
    user = os.environ["UNFI_USER"]
    password = os.environ["UNFI_PASSWORD"]
    unfi_api = UnfiAPI(user, password)
    client = UnfiApiClient(unfi_api)
    model = SearchModel
    container = MainContainer
    controller = SearchController(model, container, client)
    controller.setup()

    app = App(SearchController, container, user, password)
    app.setup()
    app.run()


class SearchModel(TkModel):
    def __init__(self, controller: Controller, container: TkContainer):
        self.controller = controller
        self.variables: Dict[str, tk.Variable] = {}
        self.products: List[UNFIProduct] = []
        self.results: Results = None

    def add_product(self, product: UNFIProduct):
        self.products.append(product)

    def add_products(self, products: List[UNFIProduct]):
        self.products.extend(products)
    
    def add_results(self, results: Results):
        self.results = results
    
    def add_result(self, result: Result):
        self.results.append_result(result)

class SearchController(Controller):
    def __init__(self, model: SearchModel, view: TkContainer, client: UnfiApiClient):
        super().__init__(model, view)
        self.client = client

    def search(self, query: str, callback: Callable = None) -> Results:
        results = []
        for chunk in list(divide_chunks(query, search_chunk_size)):
            result = self.client.search(" ".join(chunk))
            results.append(result)
        return Results(results)

    def download_products(self, result: Results, callback=None):
        return result.download_products(callback=callback)

    def save_workbook(self, products: List[UNFIProduct], callback=None):
        excel_dicts = [product.to_excel_dict() for product in products]
        dict_keys = set(sorted([key for d in excel_dicts for key in d.keys()]))


class App:
    def __init__(
        self,
        controller: SearchController,
        view: MainContainer,
        user: str,
        password: str,
        model=None,
    ):
        self.view = view
        self.controller = controller
        self.container: tk.Tk = None
        self.user = user
        self.password = password

    def register_frame(self, frame):
        self.container.register_frame(frame)

    def unregister_frame(self, frame):
        self.container.unregister_frame(frame)

    def setup(self, *args, **kwargs):
        self.controller = self.controller(self, self.user, self.password)
        self.container = self.view(self.controller, *args, **kwargs)

    def run(self):
        self.container.run()


if __name__ == "__main__":
    main()
