import frappe

class DateTime:
    """Helper functions for working with datetimes.
    """
    def convert_zammad_to_erpnext(datetime_str: str) -> str:
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