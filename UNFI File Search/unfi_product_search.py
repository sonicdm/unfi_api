from __future__ import annotations

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Callable, Dict, List, Union

# from unfi_api.api import UnfiAPI
# from unfi_api.client import UnfiApiClient
# from unfi_api.product import UNFIProduct
# from unfi_api.search.result import Result, Results
# from unfi_api.utils.collections import divide_chunks

from container import TkContainer
from controller import Controller
# from excel import create_workbook, save_workbook, write_worksheet_rows
from exceptions import UnfiApiClientNotSetException
from model import TkModel
from settings import search_chunk_size
from ui import MainContainer, StartPage
from view import View
from search import SearchController, SearchModel, SearchPage

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
    # main_view = View(name="main", frame=StartPage, controller=controller)
    controller.register_main_view(search_view)
    controller.register_view(search_view)
    controller.run()


if __name__ == "__main__":
    main()
