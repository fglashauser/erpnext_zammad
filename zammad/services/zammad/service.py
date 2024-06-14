import frappe
from abc import ABC, abstractmethod
from ...data import ZammadAPI

class Service(ABC):
    def __init__(self, api: ZammadAPI = None):
        self.settings = frappe.get_single("Zammad Settings")
        self.api = api if api else ZammadAPI(url=self.settings.api_url,
                                             http_token=self.settings.get_password("api_token"))