// Copyright (c) 2024, PC-Giga and contributors
// For license information, please see license.txt

frappe.ui.form.on("Zammad Import", {
	refresh(frm) {
        // Call frm method "start_import" when button with name "start_import" is clicked

	},

    start_import(frm) {
        frm.call('start_import');
        frappe.msgprint(__("Starting Zammad Import. This may take a while. Please watch the logs for progress.") +
            __(' <a href="/app/zammad-import-log">Click here</a> to view the Zammad Import Log'));
    },
});
