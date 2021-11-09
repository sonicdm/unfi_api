from __future__ import annotations

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Callable, Dict, List, Union

from unfi_api.api import UnfiAPI
from unfi_api.client import UnfiApiClient
from unfi_api.product import UNFIProduct
from unfi_api.search.result import Result, Results
from unfi_api.utils.collections import divide_chunks

from container import TkContainer
from controller import Controller
from excel import create_workbook, save_workbook, write_worksheet_rows
from exceptions import UnfiApiClientNotSetException
from model import TkModel
from settings import search_chunk_size
from ui import DownloadPage, MainContainer, SearchPage, StartPage
from view import View

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def main():
    user = os.environ["UNFI_USER"]
    password = os.environ["UNFI_PASSWORD"]
    # unfi_api = UnfiAPI(user, password, incapsula=False)
    # client = UnfiApiClient(unfi_api)
    client = "client"
    search_model = SearchModel
    search_model.set_client(client)
    model = TkModel
    container = MainContainer
    controller = SearchController(container, model, search_model)
    search_view = View(
        name="search", frame=SearchPage, controller=controller, model=search_model
    )
    main_view = View(name="main", frame=StartPage, controller=controller)
    download_view = View(name="download", frame=DownloadPage, controller=controller)
    controller.register_main_view(main_view)
    controller.register_view(search_view)
    controller.register_view(download_view)
    controller.run()


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
        self.results: Results = None

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


if __name__ == "__main__":
    main()
