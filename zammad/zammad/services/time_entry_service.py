from .article_service import ArticleService
from ..data import ZammadConnector
from ..zammad_settings import ZammadSettings
from .. import helpers
import frappe

class TimeEntryService:
    """Service for Time Entry related operations in Zammad.
    """
    def __init__(self, zammad_connector : ZammadConnector = None):
        """Initializes TicketService.
        If zammad_connector is not provided, it will create a new one with default settings.
        
        Args:
            zammad_connector (ZammadConnector, optional): ZammadConnector instance. Defaults to None.
        """
        self.settings = ZammadSettings()
        self.zammad = zammad_connector if zammad_connector else ZammadConnector()
        self.article_service = ArticleService(self.zammad)

    
    def _prepare_time_entries(self, time_entries):
        """Prepares the time entries for import.

        Args:
            time_entries (list): Time entries to prepare.
        Returns:
            list: Prepared time entries.
        """
        # Prepare each time entry
        for i in range(len(time_entries)):
            time_entries[i] = self._prepare_time_entry(time_entries[i])
        return time_entries


    def _prepare_time_entry(self, time_entry):
        """Prepares the time entry for import.

        Args:
            time_entry (dict): Time entry to prepare.
        Returns:
            dict: Prepared time entry.
        """
        # Set the employee (search by mapping or use default if not found)
        employee = self.settings.get_employee_by_agent_id(time_entry.get('created_by_id', None))
        if not employee:
            employee = self.settings.default_employee
        time_entry['employee'] = employee.name

        # Set the activity type (search by mapping or use default if not found)
        activity_type = self.settings.get_activity_type_by_id(time_entry.get('type_id', None))
        if not activity_type:
            activity_type = self.settings.default_activity_type
        time_entry['activity_type'] = activity_type.name

        # Set creation date & convert to local timezone
        time_entry['created_at'] = helpers.DateTime.convert_zammad_to_erpnext(time_entry.get('created_at', None))

        # Set duration (convert from hours to seconds)
        time_entry['duration'] = float(time_entry.get('time_unit', 0.0)) * 3600

        # Set the description
        article = self.article_service.get_article(time_entry.get('ticket_article_id', None))
        time_entry['description'] = article.get('body', None) if article else None

        return time_entry


    def get_time_entries(self, ticket_id: int):
        """Returns the time entries for the given ticket id.
        
        Args:
            ticket_id (int): Ticket id.
        Returns:
            list: Time entries.
        """
        # Get the time entries for the given ticket id
        time_entries = self.zammad.api.ticket_time_accounting.get_by_ticket_id(ticket_id=ticket_id)

        # Return the time entries
        return self._prepare_time_entries(time_entries)