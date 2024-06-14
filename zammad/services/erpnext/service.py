import frappe
from abc import ABC, abstractmethod

class Service(ABC):
    def __init__(self):
        self.settings = frappe.get_single("Zammad Settings")