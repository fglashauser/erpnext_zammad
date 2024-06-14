# Copyright (c) 2024, PC-Giga and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ....services import zammad
from ....services import erpnext


class ZammadImport(Document):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ticket_service = zammad.Ticket()
		self.timesheet_service = erpnext.Timesheet()
		self.import_log_service = erpnext.ImportLog()

	@frappe.whitelist()
	def start_import(self):
		"""Starts the import of Zammad data to ERPNext."""
		frappe.enqueue_doc(
			"Zammad Import",
			self.name,
			"start_import_job",
			queue="long",
			timeout=5000
		)

	def start_import_job(self):
		"""Imports Zammad data to ERPNext."""
		
		# Alle Tickets via API holen und nach Tag & Status filtern
		tickets = self._get_tickets()

		# Timesheets anlegen, Tag setzen & Log erstellen
		for ticket in tickets:
			timesheet = self._create_timesheet(ticket)
			self._set_import_tag(ticket)
			self._create_log(ticket, timesheet)
			print(f"Ticket {ticket.get('number', '???')} imported.")

		# DB-Änderungen schreiben
		frappe.db.commit()

	def _get_tickets(self) -> list:
		"""Returns all tickets from Zammad."""
		tickets = self.ticket_service.get_tickets()
		return tickets

	def _create_timesheet(self, ticket: dict) -> Document:
		"""Creates a timesheet for the ticket."""
		timesheet = self.timesheet_service.create_by_zammad_ticket(ticket)
		return timesheet.insert()

	def _set_import_tag(self, ticket: dict) -> None:
		"""Sets the import tag for the ticket."""
		self.ticket_service.set_import_tag(ticket.get('id', None))

	def _create_log(self, ticket: dict, timesheet: Document) -> Document:
		"""Creates a log for the imported tickets."""
		return self.import_log_service.log_import(ticket, timesheet)