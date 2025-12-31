# portal.py
import frappe
from frappe import _

def get_portal_menu_items():
    return [
        {
            "title": _("Compliance Status"),
            "route": "/compliance",
            "reference_doctype": "Compliance",
            "role": "Customer"
        },
        {
            "title": _("Documents"),
            "route": "/documents",
            "reference_doctype": "File",
            "role": "Customer"
        },
        {
            "title": _("Profile"),
            "route": "/profile",
            "reference_doctype": "Customer",
            "role": "Customer"
        }
    ]

@frappe.whitelist(allow_guest=True)
def get_client_compliances(customer):
    """Get compliances for a specific customer"""
    client = frappe.db.get_value("CA Client", {"customer": customer}, "name")
    
    if client:
        compliances = frappe.get_all("Compliance",
            filters={"client": client},
            fields=["compliance_type", "period", "due_date", "status", "actual_submission_date"],
            order_by="due_date desc",
            limit=20
        )
        return compliances
    
    return []
