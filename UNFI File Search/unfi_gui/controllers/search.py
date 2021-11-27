from __future__ import annotations, absolute_import
from typing import TYPE_CHECKING, Callable, List, Union

from unfi_api.product.product import UNFIProduct, UNFIProducts
from ..controller import Controller
from ..container import TkContainer
from ..settings import (
    auto_download,
    auto_login,
    auto_save,
    default_save_path,
    password,
    save_settings,
    search_chunk_size,
    update_settings,
    username,
)

from unfi_api.utils.collections import divide_chunks

if TYPE_CHECKING:
    from unfi_api.search.result import Result, Results
    from ..models.search import SearchModel
    from ..download import DownloadModel
    from ..model import TkModel
    
    
class SearchController(Controller):
    def __init__(
            self, container: TkContainer, model: TkModel, search_model: SearchModel, download_model: DownloadModel
    ):
        container = container
        self.search_model: SearchModel = search_model(self)
        self.download_model: DownloadModel = download_model(self)
        super().__init__("unfi_api_search", container, model)

    def search(self, query: str, callback: Callable = None) -> Results:
        client = self.search_model.get_client()
        results = []
        for chunk in list(divide_chunks(query, search_chunk_size)):
            self.search_model.search(chunk)

    def download_products(
            self, result: Union[Results, Result], callback=None
    ) -> UNFIProducts:
        return self.download_model.download_products(result, callback)

    def get_downloaded_products(self) -> UNFIProducts:
        return self.download_model.downloaded_products

    def save_workbook(self, products: List[UNFIProduct], callback=None):
        excel_dicts = [product.to_excel_dict() for product in products]
        dict_keys = set(sorted([key for d in excel_dicts for key in d.keys()]))