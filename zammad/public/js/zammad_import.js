frappe.ui.form.on('Zammad Import', {
    refresh: function(frm) {
        frm.add_custom_button(__('Test Import'), function () {
            // Hier könnten Sie den Aufruf der TicketService.get_all_tickets Funktion machen
            frappe.call({
                method: "zammad.zammad.doctype.zammad_import.zammad_import.get_all_tickets",
                args: {
                    // args, die Sie an die Methode übergeben wollen
                },
                callback: function(r) {
                    if(r.message) {
                        console.log(r.message);
                        frappe.msgprint(__('Tickets imported'));
                    }
                }
            });
        });
    }
});
