from __future__ import annotations
from typing import TYPE_CHECKING, Callable

from unfi_api.product.product import UNFIProducts

from .model import TkModel
from unfi_api import UnfiApiClient
from unfi_api.search.result import Results
if TYPE_CHECKING:
    from .controller import Controller

class DownloadModel(TkModel):
    client: UnfiApiClient = None

    def __init__(self, controller: Controller):
        self.event_types = ["startDownload", "onDownload", "onDownloadComplete", "onDownloadError", "onCancel"]
        super().__init__(controller)
        self.downloaded_products: UNFIProducts = UNFIProducts()
        self.download_queue = []
        cancel_fn = lambda x: controller.stop_job(x) if x in controller.cancel else None
        self.register_event_handler("onDownload", controller.stop_cancelled_jobs)
        self.job_id = None

    @classmethod
    def set_client(cls, client: UnfiApiClient):
        cls.client = client

    @classmethod
    def get_client(cls) -> UnfiApiClient:
        return cls.client


    def download_products(self, results: Results, callback: Callable = None, progress_callback: Callable = None):
        def _dl_callback(x):
            self.trigger_event("onDownload", x)
            if callback:
                callback(x)
        job_id = "product_download"
        products = results.download_products(self.client, callback=lambda x:_dl_callback(job_id), threaded=True, thread_count=10, job_id=job_id)
        self.downloaded_products.update(products)
    
    def cancel_download(self):
        pass