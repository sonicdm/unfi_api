from . import reports, user


class AdminBackend(object):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """
    def __init__(self, api):
        self.api = api
        self.user = User(api)
        self.reports = Reports(api)
        pass


class User(object):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api):
        self.api = api

    def insert_selected_account_as_default(self, account_number):
        token = self.api.auth_token
        account_number = self.api.account
        user_id = self.api.user_id
        region = self.api.account_region
        warehouse = self.api.warehouse,
        account_result = user.insert_selected_account_as_default(token, user_id, account_number, region)
        return account_result


class Reports(object):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api):
        self.api = api
