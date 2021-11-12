
from __future__ import annotations
from typing import TYPE_CHECKING
from unfi_api.api.admin_backend import reports, user
from unfi_api.api.base_classes import Endpoint, APICore
if TYPE_CHECKING:
    from unfi_api import UnfiAPI
    

class AdminBackend(Endpoint):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api: APICore):
        self.name = "admin_backend"
        self.api: APICore = api
        self.api.register_endpoint(self)
        self.user: Endpoint = User(api)
        self.reports: Endpoint = Reports(api)
        pass


class User(Endpoint):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api: 'UnfiAPI'):
        self.name = "user"
        self.api = api
        self.api.register_endpoint(self)

    def insert_selected_account_as_default(self, account_number):
        token = self.api.auth_token
        account_number = self.api.account
        user_id = self.api.user_id
        region = self.api.account_region
        warehouse = self.api.warehouse,
        account_result = user.insert_selected_account_as_default(token, user_id, account_number, region)
        self.api.refresh_metadata()
        return account_result

    def get_users_data(self):
        token = self.api.auth_token
        user_id = self.api.user_id
        return user.get_users_data(token, user_id)


class Reports(Endpoint):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api: APICore):
        self.name = "reports"
        self.api: APICore = api
        self.api.register_endpoint(self)