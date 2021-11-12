from __future__ import annotations
from logging import log
from typing import TYPE_CHECKING, List, Dict, Union, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from unfi_api.utils.threading import threader
import concurrent.futures.thread
from unfi_api.invoice import OrderListing

from unfi_api.product import UNFIProducts
from unfi_api.utils.logging import get_logger, set_log_path

logger = get_logger(__name__)


if TYPE_CHECKING:
    from unfi_api import UnfiAPI, UnfiApiClient
    from unfi_api.product import UNFIProduct
    from unfi_api.search.result import ProductResult, Results


def download_products(
    client: "UnfiApiClient",
    product_results: List["ProductResult"],
    callback=None,
    threaded: bool = False,
    thread_count: int = 4,
) -> Dict[str, UNFIProduct]:
    products = {}
    print(f"Downloading {len(product_results)} products...", end=" ")
    if threaded:
        result: List[UNFIProduct] = threader(client.get_product, product_results, callback, thread_count)
        for res in result:
            products[res.product_code] = res

    else:
        for product in product_results:
            product = product.download(client)
            products[product.product_code] = product
            callback(product)
    print(f"Downloaded {len(products)} products")
    print(f"Compiling {len(products)}...", end=" ")
    unfi_products = UNFIProducts(products)
    print("Done.")
    return unfi_products


def download_invoices(
    client: "UnfiApiClient",
    invoices: List[Union[OrderListing, str]],
    callback: Callable=None,
    threaded: bool = False,
    thread_count: int = 4,
) -> List[str]:

    if threaded:
        results = threader(client.get_invoice, invoices, callback, thread_count)
    else:
        results = []
        for invoice in invoices:
            result = client.get_invoice(invoice)
            results.append(result)
            if callback:
                callback(result)
    

    return results