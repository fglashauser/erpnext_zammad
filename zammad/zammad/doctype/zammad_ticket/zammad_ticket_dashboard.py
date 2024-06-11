from frappe import _

def get_data():
    return {
        'fieldname': 'ticket',
        'transactions': [
            {
                'label': _('Time Entries'),
                'items': ['Zammad Time Entry']
            }
        ]
    }
