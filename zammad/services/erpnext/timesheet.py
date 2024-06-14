import frappe
from frappe.model.document import Document
from . import Service
from .tools import Tools
from .. import zammad
from .time_log import TimeLog

class Timesheet(Service):
    """Service for timesheet related operations in ERPNext.
    """
    def __init__(self):
        super().__init__()
        self.tools = Tools()
        self.article_service = zammad.Article()
        self.time_log_service = TimeLog()


    def create_by_zammad_ticket(self, ticket: dict) -> Document:
        """Returns a new ERPNext timesheet document by the given Zammad ticket.
        
        Args:
            ticket (dict): Zammad ticket.
        Returns:
            frappe.Document: Timesheet document
        """
        # Contact
        contact = self.tools.get_contact_by_email(ticket.get('customer', None))
        if not contact:
            contact = frappe.get_doc('Contact', self.settings.default_contact)

        # Customer
        customer = self.tools.get_customer_by_contact(contact) if contact else None

        # Employee
        employee = self.tools.get_employee_by_email(ticket.get('owner', None))
        if not employee:
            employee = frappe.get_doc('Employee', self.settings.default_employee)

        # Generate timesheet
        timesheet = frappe.get_doc({
            "doctype": "Timesheet",
            "title": f"#{ticket.get('number', str())}: {ticket.get('title', str())}",
            "company": self.settings.company,
            "custom_contact": contact.name if contact else None,
            "customer": customer.name if customer else None,
            "employee": employee.name if employee else None,
            "note": self.article_service.get_ticket_description(ticket),
            "time_logs": self.time_log_service.create_by_zammad_ticket(ticket)
        })

        return timesheet