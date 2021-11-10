from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict, Union, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures.thread

from unfi_api.product import UNFIProducts

if TYPE_CHECKING:
    from unfi_api import UnfiAPI, UnfiApiClient
    from unfi_api.product import UNFIProduct
    from unfi_api.search.result  import ProductResult, Results
    
def download_products(
    client: 'UnfiApiClient',
    product_results: List['ProductResult'],
    callback=None,
    threaded: bool = False,
    thread_count: int = 4,
) -> Dict[str, UNFIProduct]:
    products = {}

    if threaded:
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            try:
                futures = [
                    executor.submit(product.download, client)
                    for product in product_results
                ]
                # done, not_done = wait(futures, timeout=0)
                for future in as_completed(futures):
                    try:
                        product = future.result()
                        products[product.product_code] = product
                        callback(product)
                        if all([future.done() for future in futures]):
                            break
                    except Exception as e:
                        print(e)
                        raise
                    except KeyboardInterrupt:
                        executor.shutdown(wait=False)
            except KeyboardInterrupt:
                executor._threads.clear()
                concurrent.futures.thread._threads_queues.clear()
                raise

    else:
        for product in product_results:
                product = product.download(client)
                products[product.product_code] = product
                callback(product)
    return UNFIProducts(products)