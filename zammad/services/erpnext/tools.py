import frappe
import frappe.utils
from frappe.model.document import Document
from . import Service

class Tools(Service):
    """Service for ticket / timesheet related operations in ERPNext.
    """

    def get_contact_by_email(self, email: str) -> Document:
        """Returns the ERPNext contact document by the given email.
        
        Args:
            email (str): Email address.
        Returns:
            frappe.Document: Contact document or None if not found.
        """
        # Search for a contact with the given email
        contact_name = frappe.db.sql("""
            SELECT parent
            FROM `tabContact Email`
            WHERE email_id = %s
        """, (email), as_dict=True)

        # If a contact was found, return it
        if contact_name:
            return frappe.get_doc('Contact', contact_name[0]['parent'])

        # No result found, return None
        return None
    

    def get_customer_by_contact(self, contact: Document) -> Document:
        """Returns the ERPNext customer document by the given contact.
        
        Args:
            contact (str): Contact.
        Returns:
            frappe.Document: Customer document or None if not found.
        """
        for link in contact.links:
            if link.link_doctype == 'Customer':
                return frappe.get_doc('Customer', link.link_name)

        # No result found, return None
        return None


    def get_employee_by_email(self, email: str) -> Document:
        """Returns the ERPNext employee document by the given email.
        
        Args:
            email (str): Email address.
        Returns:
            frappe.Document: Employee document or None if not found.
        """
        # Search for an employee with the given email
        employees = frappe.get_list('Employee', filters={'company_email': email}, fields=['name'])

        # If an employee was found, return it
        if employees:
            # Return first employee found
            return frappe.get_doc('Employee', employees[0].name)

        # No result found, return None
        return None


    def convert_datetime_from_zammad(self, datetime_str: str) -> str:
        """Converts the given datetime string from Zammad to ERPNext format.
        
        Args:
            datetime_str (str): Datetime string in Zammad format.
        Returns:
            str: Datetime string in ERPNext format.
            Returns None if no valid data is given.
        """
        if not datetime_str:
            return None

        datetime = frappe.utils.get_datetime(datetime_str).replace(tzinfo=None)
        return frappe.utils.convert_utc_to_system_timezone(datetime).strftime('%Y-%m-%d %H:%M:%S')