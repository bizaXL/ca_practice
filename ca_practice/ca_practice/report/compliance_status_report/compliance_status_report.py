import frappe

def execute(filters=None):
    columns = [
        {"fieldname": "client", "label": "Client", "fieldtype": "Link", "options": "CA Client", "width": 200},
        {"fieldname": "compliance_type", "label": "Compliance Type", "fieldtype": "Data", "width": 150},
        {"fieldname": "period", "label": "Period", "fieldtype": "Data", "width": 120},
        {"fieldname": "due_date", "label": "Due Date", "fieldtype": "Date", "width": 100},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 100}
    ]
    data = frappe.db.get_all("Compliance", fields=["client", "compliance_type", "period", "due_date", "status"])
    return columns, data
