# zammad/zammad/doctype/zammad_import/zammad_import.py
import frappe
from frappe.utils import getdate, formatdate, format_time, now
from zammad.zammad.services import TicketService, TimeEntryService

@frappe.whitelist()
def fetch_tickets(docname, ticket_state : str = 'All', only_billable : bool = False):
    """Fetches tickets from Zammad by the given filters.
    Fetches only tickets that don't have the import tag set.

    Args:
        docname (str): Name of the document to which the tickets should be added.
        ticket_state (str, optional): Ticket state filter. Defaults to 'All'.
            Possible options: All, Open, Closed
        only_billable (bool, optional): If true, only billable tickets will be fetched. Defaults to False.
    """
    ticket_service = TicketService()
    tickets = ticket_service.fetch_tickets(ticket_state, only_billable)
    
    # Add fetched tickets to the child table of the given document
    add_tickets_to_child_table(docname, tickets)

    return {'message': f'{len(tickets)} tickets fetched and added.'}


@frappe.whitelist()
def add_tickets_to_child_table(docname, tickets):
    """Adds the tickets to the child table of the given document.

    Args:
        docname (str): Name of the document to which the tickets should be added.
        tickets (list of dict): A list of tickets to add to the child table.
    """
    time_entry_service = TimeEntryService()
    doc = frappe.get_doc("Zammad Import", docname)
    
    # Remove all existing child table entries
    doc.set('zammad_tickets', [])
    
    for ticket in tickets:
        # Create a new child table entry
        child_entry = frappe.get_doc({
            'doctype'           : 'Zammad Ticket',
            'parenttype'        : 'Zammad Import',
            'parentfield'       : 'zammad_tickets',
            'zammad_ticket_id'  : ticket.get('id', None),
            'customer_contact'  : ticket.get('customer_contact', None),
            'number'            : ticket.get('number', None),
            'title'             : ticket.get('title', None),
            'employee'          : ticket.get('employee', None),
            'created_at'        : ticket.get('created_at', None),
            'closed_at'         : ticket.get('close_at', None),
            'description'       : ticket.get('description', None)
        })
        # Add the child table entry to the document
        doc.append('zammad_tickets', child_entry)
    
    # Save the document
    doc.save()

    # Insert Time Entries for every ticket
    for ticket in doc.zammad_tickets:
        # Fetch time entries for the ticket
        time_entries = time_entry_service.get_time_entries(ticket.zammad_ticket_id)

        # Add time entries
        for time_entry in time_entries:
            # Create a new time entry document
            doc_time_entry = frappe.get_doc({
                'doctype'            : 'Zammad Time Entry',
                'ticket'            : ticket.get('name', None),
                'employee'          : time_entry.get('employee', None),
                'activity_type'     : time_entry.get('activity_type', None),
                'created_at'        : time_entry.get('created_at', None),
                'duration'          : time_entry.get('duration', None),
                'description'       : time_entry.get('description', None)
            })
            # Create a new document for the time entry
            doc_time_entry.save()
