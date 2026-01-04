import frappe
from frappe import _

def get_context(context):
    context.title = _("Documents")
    context.documents = get_documents()

def get_documents():
    user = frappe.session.user
    
    # 1. Find Contact first
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

    # 3. Find CA Client
    client = frappe.db.get_value("CA Client", {"customer": customer}, "name")
    
    if not client:
        return []

    return frappe.get_all("CA Client Document",
        filters={"parent": client, "parenttype": "CA Client", "parentfield": "documents_attached"},
        fields=["document_name", "attachment", "uploaded_on"],
        order_by="uploaded_on desc"
    )
