import frappe
from frappe import _

def get_context(context):
    context.title = _("Compliance Status")
    context.compliances = get_compliances()

def get_compliances():
    user = frappe.session.user
    
    # 1. Find Contact linked to this User email
    contact = frappe.db.get_value("Contact", {"email_id": user}, "name")
    if not contact:
        return []

    # 2. Find Customer linked to that Contact
    customer = frappe.db.get_value("Dynamic Link", {
        "parent": contact,
        "link_doctype": "Customer",
        "parenttype": "Contact"
    }, "link_name")

    if not customer:
        return []

    # 3. Find CA Client Linked to Customer
    client = frappe.db.get_value("CA Client", {"customer": customer}, "name")
    
    if not client:
        return []

    return frappe.get_all("Compliance",
        filters={"client": client},
        fields=["compliance_type", "period", "due_date", "status", "actual_submission_date"],
        order_by="due_date asc"
    )
