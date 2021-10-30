
from abc import ABC


class APICore(ABC):
    """Base for API Object"""

    def __init__(self):
        self.warehouse_id = None
        self.session = None
        self.warehouse = None
        self.account_region = None
        self.user_id = None
        self.account = None
        self.auth_token = None
        self.logged_in = False



class Endpoint:
    """Base for API Endpoint"""