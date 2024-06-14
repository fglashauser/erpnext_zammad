from .article import Article
from . import Service
import frappe

class TimeEntry(Service):

    def get_time_entries(self, ticket_id: int) -> list:
        """Returns the time entries for the given ticket id.
        
        Args:
            ticket_id (int): Ticket id.
        Returns:
            list: Time entries.
        """
        # Get the time entries for the given ticket id
        time_entries = self.api.ticket_time_accounting.get_by_ticket_id(ticket_id=ticket_id)
        return time_entries