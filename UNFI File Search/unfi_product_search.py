import os
from tkinter import tk
from ui import StartPage, MainContainer
from unfi_api import UnfiAPI, UnfiApiClient
from unfi_api.search.result import Result


def main():
    container = MainContainer
    app = App()


class SearchController:
    def __init__(self, model, user=None, password=None):
        if user is None:
            user = os.environ.get('UNFI_USER')
        if password is None:
            password = os.environ.get('UNFI_PASSWORD')
        self.api = UnfiAPI(user, password)
        self.client = UnfiApiClient(self.api)

    def search(self, query: str):
        return self.client.search(query)

    def download_products(self, result: Result, callback=None):
        return result.download_products()

class App:
    def __init__(self, controller, view, model):
        self.view = view
        self.controller = controller
        self.container: tk.Tk = None

    def register_frame(self, frame):
        self.container.register_frame(frame)

    def unregister_frame(self, frame):
        self.container.unregister_frame(frame)

    def setup(self, *args, user=None, password=None, **kwargs):
        self.container = self.view(*args, controller=self.controller, **kwargs)

    def run(self):
        self.container.run()


if __name__ == "__main__":
    main()
