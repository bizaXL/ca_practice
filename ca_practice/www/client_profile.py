import frappe
from frappe import _

def get_context(context):
    context.title = _("Profile")
    context.client = get_client_profile()

def get_client_profile():
    user = frappe.session.user
    
    # 1. Find Contact first
    contact = frappe.db.get_value("Contact", {"email_id": user}, "name")
    if not contact:
        return None

    # 2. Find Customer linked to that Contact
    customer = frappe.db.get_value("Dynamic Link", {
        "parent": contact, 
        "link_doctype": "Customer", 
        "parenttype": "Contact"
    }, "link_name")

    if not customer:
        return None

    # 3. Find full CA Client document
    client_name = frappe.db.get_value("CA Client", {"customer": customer}, "name")
    
    if not client_name:
        return None
        
    return frappe.get_doc("CA Client", client_name)
