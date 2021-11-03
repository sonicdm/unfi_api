from abc import ABC, abstractmethod, abstractproperty

import requests


class Endpoint:
    """Base for API Endpoint"""
    endpoint: str
    name: str


class APICore(ABC):
    """Base for API Object"""

    session: requests.Session

    @abstractmethod
    def register_endpoint(self, endpoint: Endpoint):
        """Register an endpoint"""

    @abstractmethod
    def get(self, url: str, params: dict = None, **kwargs) -> requests.Response:
        """
        gets a url with params
        """
        pass

    # passes post method to requests.Session.post()
    @abstractmethod
    def post(self, url: str, data: dict = None, **kwargs) -> requests.Response:
        """
        posts to a url with data
        """
        pass

    @abstractmethod
    def put(self, url: str, data: dict = None, **kwargs) -> requests.Response:
        """
        puts to a url with data
        """
        pass

    @abstractmethod
    def login(self, username: str, password: str) -> requests.Response:
        """
        logs in to the api and sets self.logged_in to True if successful
        """
        pass

    @abstractmethod
    def logout(self) -> requests.Response:
        """
        logs out of the api and sets self.logged_in to False if successful
        """
        pass

    @abstractmethod
    def is_logged_in(self) -> bool:
        """
        returns True if logged in, False if not
        """
        pass

    @abstractmethod
    def get_session(self) -> requests.Session:
        """
        returns the requests.Session object
        """
        pass

    @abstractmethod
    def set_session(self, session: requests.Session) -> None:
        """
        sets the session object
        """
        pass

    @property
    @abstractmethod
    def cookies(self) -> dict:
        """
        returns the cookies dict
        """
        pass

    @cookies.setter
    @abstractmethod
    def cookies(self, cookies: dict) -> None:
        """
        sets the cookies dict
        """
        pass

    @property
    @abstractmethod
    def headers(self) -> dict:
        """
        returns the headers dict
        """
        pass

    @headers.setter
    @abstractmethod
    def headers(self, headers: dict) -> None:
        """
        sets the headers dict
        """
        pass
