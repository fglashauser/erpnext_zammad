import frappe
from frappe.utils.password import get_decrypted_password
from .helpers.singleton import Singleton

class ZammadSettings(metaclass=Singleton):
    def __init__(self):
        self._settings = frappe.get_single("Zammad Settings")


    @property
    def api_url(self) -> str:
        return self._settings.api_url
    

    @property
    def auth_token(self) -> str:
        return get_decrypted_password("Zammad Settings", "Zammad Settings",
                                        fieldname="auth_token")


    @property
    def default_employee(self):
        return frappe.get_doc("Employee", self._settings.default_employee)


    @property
    def default_activity_type(self):
        return frappe.get_doc("Activity Type", self._settings.default_activity_type)


    @property
    def import_tag(self) -> str:
        return self._settings.import_tag


    def get_employee_by_agent_id(self, id: int):
        """Returns the employee document by the given agent id.
        
        Args:
            id (int): Agent id.
        Returns:
            frappe.Document: Employee document or None if not found.
        """
        # Search for a matching mapping
        matching_mapping = next(
            (mapping for mapping in self._settings.agent_employee_mapping \
             if str(mapping.zammad_agent_id) == str(id)), None)

        # If matching mapping found, return the employee
        if matching_mapping:
            return frappe.get_doc("Employee", matching_mapping.employee)
        
        # If no matching mapping found, return None
        return None


    def get_activity_type_by_id(self, id: int):
        """Returns the activity type document by the given Zammad id.
        
        Args:
            id (int): Activity type id.
        Returns:
            frappe.Document: Activity type document or None if not found.
        """
        # Search for a matching mapping
        matching_mapping = next(
            (mapping for mapping in self._settings.activity_type_mapping \
             if str(mapping.zammad_activity_type_id) == str(id)), None)

        # If matching mapping found, return the activity type
        if matching_mapping:
            return frappe.get_doc("Activity Type", matching_mapping.activity_type)
        
        # If no matching mapping found, return None
        return None