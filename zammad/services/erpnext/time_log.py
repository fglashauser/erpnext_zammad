import frappe
from frappe.model.document import Document
from .service import Service
from .. import zammad
from .tools import Tools
from datetime import datetime, timedelta

class TimeLog(Service):
    """Service for time log related operations in ERPNext.
    """
    def __init__(self):
        super().__init__()
        self.time_entry_service = zammad.TimeEntry()
        self.article_service = zammad.Article()
        self.tools = Tools()


    def get_activity_type_by_zammad_id(self, zammad_id: int) -> str:
        """Returns the ERPNext activity type name by the given Zammad id.
        
        Args:
            zammad_id (int): Zammad activity type id.
        Returns:
            str: ERPNext activity type name.
        """
        # Search for a matching mapping
        matching_mapping = next(
            (mapping for mapping in self.settings.activity_type_map \
             if str(mapping.zammad_id) == str(zammad_id)), None)
        
        # If matching mapping found, return the activity type
        if matching_mapping:
            return matching_mapping.activity_type
        
        # If no matching mapping found, return None
        return None
    

    def create_by_zammad_ticket(self, ticket: dict) -> list[dict]:
        """Creates new ERPNext time logs by the given Zammad ticket.
        
        Args:
            ticket (dict): Zammad ticket.
        Returns:
            list[dict]: Time logs
        """
        # Get time entries
        time_entries = self.time_entry_service.get_time_entries(ticket.get('id', None))
        if not time_entries:
            return []
        
        # Generate time logs
        time_logs = []
        for time_entry in time_entries:
            activity_type = self.get_activity_type_by_zammad_id(time_entry.get('type_id', 0))
            if not activity_type:
                activity_type = self.settings.default_activity_type

            hours = float(time_entry.get('time_unit', 0.0))
            hours = hours if hours > 0 else 0.0
            to_time_str = self.tools.convert_datetime_from_zammad(time_entry.get('created_at', None))
            to_time = datetime.strptime(to_time_str, "%Y-%m-%d %H:%M:%S") if to_time_str else None
            from_time = to_time - timedelta(hours=hours) if to_time else None

            time_log = {
                "activity_type": activity_type,
                "from_time": from_time,
                "to_time": to_time,
                "hours": hours,
                "billing_hours": hours,
                "description": self.article_service.get_article_body(time_entry.get('ticket_article_id', None)),
                "completed": 1,
                "is_billable": 1,
            }
            time_logs.append(time_log)

        return time_logs