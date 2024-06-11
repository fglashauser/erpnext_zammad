from .customer_service import CustomerService
from .article_service import ArticleService
from ..data import ZammadConnector
from ..zammad_settings import ZammadSettings
from .. import helpers
import frappe

class TicketService:
    """Service for ticket related operations in Zammad.
    """
    def __init__(self, zammad_connector : ZammadConnector = None):
        """Initializes TicketService.
        If zammad_connector is not provided, it will create a new one with default settings.
        
        Args:
            zammad_connector (ZammadConnector, optional): ZammadConnector instance. Defaults to None.
        """
        self.settings           = ZammadSettings()
        self.zammad             = zammad_connector if zammad_connector else ZammadConnector()
        self.customer_service   = CustomerService(self.zammad)
        self.article_service    = ArticleService(self.zammad)


    def _prepare_ticket(self, ticket: dict) -> dict:
        """Prepares the ticket for import.
        
        Args:
            ticket (dict): Ticket to prepare.
        Returns:
            dict: Prepared ticket.
        """
        # Search the customer contact by email
        customer_contact = self.customer_service.get_contact_by_email(ticket.get('customer', None))
        ticket['customer_contact'] = customer_contact.name if customer_contact else None

        # Set the employee (search by mapping or use default if not found)
        employee = self.settings.get_employee_by_agent_id(ticket.get('owner_id', None))
        if not employee:
            employee = self.settings.default_employee
        ticket['employee'] = employee.name

        # Set the created_at date & convert to local timezone
        ticket['created_at'] = helpers.DateTime.convert_zammad_to_erpnext(ticket.get('created_at', None))

        # Set the closed_at date & convert to local timezone
        ticket['close_at'] = helpers.DateTime.convert_zammad_to_erpnext(ticket.get('close_at', None))

        # Set the description
        description = str()
        article_ids = ticket.get('article_ids', None)
        if article_ids:
            article = self.article_service.get_article(article_ids[0])
            description = article.get('body', None)
        ticket['description'] = description

        return ticket


    def _prepare_tickets(self, tickets : list) -> list:
        """Prepares the tickets for import.
        
        Args:
            tickets (list): Tickets to prepare.
        Returns:
            list: Prepared tickets.
        """
        for i in range(len(tickets)):
            tickets[i] = self._prepare_ticket(tickets[i])
        return tickets


    def fetch_tickets(self, ticket_state : str = 'All', only_billable : bool = False) -> list:
        """Fetches tickets from Zammad by the given filters.
        Fetches only tickets that don't have the import tag set.
        
        Args:
            ticket_state (str, optional): Ticket state filter. Defaults to 'All'.
                Possible options: All, Open, Closed
            only_billable (bool, optional): If true, only billable tickets will be fetched. Defaults to False.
        Returns:
            list: List of tickets
        """
        tickets = self.zammad.api.ticket.all()
        return self._prepare_tickets(tickets)