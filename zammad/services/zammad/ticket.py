from .time_entry import TimeEntry
from . import Service

class Ticket(Service):
    """Service for ticket related operations in Zammad.
    """
    def __init__(self):
        super().__init__()
        self.time_entry_service = TimeEntry()


    def get_tickets(self) -> list:
        """Fetches tickets from Zammad by the given filters in the Zammad Settings.
        Fetches only tickets that don't have the import tag set.
        
        Returns:
            list: List of tickets
        """
        # Get all tickets from Zammad
        all_tickets = []
        current_page = self.api.ticket.all()

        while current_page:
            all_tickets.extend(current_page)
            current_page = current_page.next_page()

        # Filter tickets by tags and status
        filtered_tickets = []
        only_closed = self.settings.only_closed_tickets
        blacklist_tags = [tag.tag for tag in self.settings.blacklist_tags]
        blacklist_tags.append(self.settings.import_tag)
        for ticket in all_tickets:

            # Check if state is valid for import
            if only_closed and ticket.get('state', None) != "closed":
                continue

            # Check if ticket has the import tag or a blacklist tag
            tags = self.api.ticket.tags(ticket.get('id', None)).get('tags', None)
            if any(tag in tags for tag in blacklist_tags):
                continue
                
            # Check if ticket has time entries
            if len(ticket.get('ticket_time_accounting_ids')) == 0:
                continue

            filtered_tickets.append(ticket)
        
        return filtered_tickets
    

    def set_import_tag(self, ticket_id: int) -> None:
        """Sets the import tag to the ticket with the given id.
        
        Args:
            ticket_id (int): Ticket id.
        """
        self.api.ticket.add_tag(ticket_id, self.settings.import_tag)
        