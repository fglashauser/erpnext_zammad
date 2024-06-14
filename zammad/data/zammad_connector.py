import frappe
from .zammad_api import ZammadAPI

class ZammadConnector:
    def __init__(self, api_url : str = None, auth_token : str = None):
        """Initializes Zammad connector.
        If api_url and auth_token are not provided, it will use the values
        from DocType Zammad Settings.

        Args:
            api_url (str, optional): Zammad API URL. Defaults to None.
            auth_token (str, optional): Zammad API Auth Token. Defaults to None.
        """
        if api_url and auth_token:
            self._api = ZammadAPI(url=api_url, http_token=auth_token)
        else:
            settings = frappe.get_single("Zammad Settings")
            self._api = ZammadAPI(url=settings.api_url,
                                 http_token=settings.get_password("api_token"))
        
    @property
    def api(self):
        return self._api