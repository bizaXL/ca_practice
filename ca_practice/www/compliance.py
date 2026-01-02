import frappe
from frappe import _
def get_context(context):
    context.title = _("Compliance Status")
    context.compliances = get_compliances()
def get_compliances():
    user = frappe.session.user
    # Assuming the logged in user is the customer or linked to one
    # First try to find customer by user link if exists, or email
    customer = frappe.db.get_value("Customer", {"email_id": user}, "name")
    
    if not customer:
        # Fallback: maybe the user IS the contact linked to a customer?
        contact = frappe.db.get_value("Contact", {"email_id": user}, "name")
        if contact:
            # Check links
            customer = frappe.db.get_value("Dynamic Link", {
                "parent": contact, 
                "link_doctype": "Customer", 
                "parenttype": "Contact"
            }, "link_name")
    if not customer:
        return []
    client = frappe.db.get_value("CA Client", {"customer": customer}, "name")
    
    if not client:
        return []
    return frappe.get_all("Compliance",
        filters={"client": client},
        fields=["compliance_type", "period", "due_date", "status", "actual_submission_date"],
        order_by="due_date asc"
    )
