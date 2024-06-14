from .service import Service
import frappe
from frappe.model.document import Document

class ImportLog(Service):
    """Service for import log related operations in ERPNext.
    """
    
    def log_import(self, ticket: dict, timesheet: Document) -> Document:
        """Logs the import of the given Zammad ticket and timesheet.
        
        Args:
            ticket (dict): Zammad ticket.
            timesheet (frappe.Document): Timesheet.
        """
        # Log the import
        return frappe.get_doc({
            "doctype": "Zammad Import Log",
            "import_datetime": frappe.utils.now(),
            "ticket_number": ticket.get('number', str()),
            "ticket_title": ticket.get('title', str()),
            "timesheet": timesheet.name,
        }).insert()