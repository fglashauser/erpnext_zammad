from ..data import ZammadConnector
from ..zammad_settings import ZammadSettings
import frappe

class CustomerService:
    """Service for customer related operations in Zammad.
    """
    def __init__(self, zammad_connector : ZammadConnector = None):
        """Initializes CustomerService.
        If zammad_connector is not provided, it will create a new one with default settings.
        
        Args:
            zammad_connector (ZammadConnector, optional): ZammadConnector instance. Defaults to None.
        """
        self.settings = ZammadSettings()
        self.zammad = zammad_connector if zammad_connector else ZammadConnector()

    
    def get_contact_by_email(self, email: str):
        """Returns the ERPNext contact document by the given email.
        
        Args:
            email (str): Email address.
        Returns:
            frappe.Document: Contact document or None if not found.
        """
        # Search for a contact with the given email
        contacts = frappe.get_list('Contact', filters={'email_id': email}, fields=['name'])

        # If a contact was found, return it
        if contacts:
            # Return first contact found
            return frappe.get_doc('Contact', contacts[0].name)

        # No result found, return None
        return None