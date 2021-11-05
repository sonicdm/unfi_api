import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from typing import List, Union
from ui import StartPage, MainContainer
from unfi_api import UnfiAPI, UnfiApiClient
from unfi_api.product import UNFIProduct
from unfi_api.search.result import Result, Results
from excel import create_workbook, save_workbook, write_worksheet_rows
from settings import search_chunk_size
from unfi_api.utils.collections import divide_chunks

def main():
    container = MainContainer
    user = os.environ['UNFI_USER']
    password = os.environ['UNFI_PASSWORD']
    app = App(SearchController, container, user, password)
    app.setup()
    app.run()




class SearchController:
    def __init__(self, model, user=None, password=None):
        if user is None:
            user = os.environ.get('UNFI_USER')
        if password is None:
            password = os.environ.get('UNFI_PASSWORD')
        self.api = UnfiAPI(user, password)
        self.client = UnfiApiClient(self.api)

    def search(self, query: str) -> Results:
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
    def __init__(self, controller: SearchController, view: MainContainer, user: str, password:str, model=None):
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
