import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class CAClient(Document):
    def validate(self):
        self.set_title()
        
    def set_title(self):
        if self.client_name and self.client_code:
            self.title = f"{self.client_code} - {self.client_name}"
        elif self.client_name:
            self.title = self.client_name
            
    def on_update(self):
        # Update customer record with CA specific fields
        if self.customer:
            customer = frappe.get_doc("Customer", self.customer)
            customer.custom_ca_client = self.name
            customer.custom_client_type = self.client_type
            customer.save(ignore_permissions=True)

@frappe.whitelist()
def create_engagement(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc
    
    def set_missing_values(source, target):
        target.engagement_date = nowdate()
        target.status = "Draft"
        
    doc = get_mapped_doc("CA Client", source_name, {
        "CA Client": {
            "doctype": "CA Engagement",
            "field_map": {
                "name": "client",
                "client_name": "client_name",
                "engagement_partner": "engagement_partner"
            }
        }
    }, target_doc, set_missing_values)
    
    return doc
