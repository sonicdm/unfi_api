
from typing import Callable, Dict, List
from functools import reduce
from unfi_api import UnfiApiClient
from unfi_api.product import UNFIProduct
from unfi_api.product.product import ProductListing
from unfi_api.search.result import Result, Results
from unfi_api.utils.string import divide_list_into_chunks_by_character_limit
from unfi_api.utils.threading import threader
from ..settings import search_chunk_size
from ..controller import Controller
from ..exceptions import UnfiApiClientNotSetException
from ..model import TkModel


class SearchModel(TkModel):
    """
    usage:
    """

    client: UnfiApiClient = None

    def __init__(self, controller: Controller, client: UnfiApiClient = None):
        self.event_types = ["onSearch", "onSearchComplete", "onSearchError", "onCancel"]
        super().__init__(controller)
        if not self.get_client() and not client:
            raise UnfiApiClientNotSetException("Client not set")
        elif not self.client and client:
            self.client = client
        self.search_terms = []
        self.searched_terms = []
        self.query_length_limit = search_chunk_size
        self.controller = controller
        self.results: Results = []
        self.search_chunk_size = search_chunk_size
        self.register_event_handler("onSearchComplete", lambda x: controller.stop_cancelled_jobs())

    
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

    def under_query_length_limit(self, query_list: List[str]) -> bool:
        query_str = " ".join(query_list)
        if len(query_str) > self.query_length_limit:
            return False
        return True

    def remove_already_searched_terms(self, terms: List[str]) -> List[str]:
        return list(filter(lambda x: x.strip() != "" and x not in self.searched_terms, terms))

    def search(self, query_list: List[str], limit: int = None, threaded: bool = False, callback: Callable = None,
               progress_callback=None, job_id="search") -> Results:
        
        self.trigger_event("onSearch", (query_list, limit, threaded, callback, progress_callback))
        def search_chunk(chunk):
            nonlocal searched_count
            nonlocal found_count
            result = chunk

            if progress_callback:
                progress_callback(result, searched_count, total_terms, found_count)
            if callback:
                callback(result)
            self.trigger_event("onSearchComplete", result)
            return result

        query_str = " ".join(query_list)
        results = []
        if self.under_query_length_limit(query_str):
            self.search_terms.append(query_list)
        else:
            query_chunks = divide_list_into_chunks_by_character_limit(query_list, self.query_length_limit)
            self.search_terms.extend(query_chunks)
        searched_count = 0
        total_terms = reduce(lambda count, element: count + len(element), self.search_terms, 0)
        found_count = 0
        if threaded:
            results = threader(search_chunk, self.search_terms, limit=limit, callback=callback)
            self.search_terms = []
        else:
            while self.search_terms:
                query_chunk = self.search_terms.pop(0)
                
                result = search_chunk(query_chunk)
                self.results.extend(result)
                self.trigger_event("onSearchComplete", result)
                if self.controller.cancel_all or job_id in self.controller.cancel:
                    break
                
    def get_description_mapped_results(self) -> Dict[str,ProductListing]:
        return {f"{product.product_code}: {product.brand} - {product.description}": product for product in self.products}

