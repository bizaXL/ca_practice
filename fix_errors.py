import frappe
import os
import json
def fix_compliance_json():
    print("Fixing Compliance DocType...")
    file_path = "apps/ca_practice/ca_practice/ca_practice/doctype/compliance/compliance.json"
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return
    with open(file_path, "r") as f:
        doc = json.load(f)
    fields = [f["fieldname"] for f in doc["fields"]]
    
    if "task_created" not in fields:
        doc["fields"].append({
            "fieldname": "task_created",
            "label": "Task Created",
            "fieldtype": "Check",
            "hidden": 1,
            "read_only": 1
        })
        print("Added task_created field")
    if "task_link" not in fields:
        doc["fields"].append({
            "fieldname": "task_link",
            "label": "Task Link",
            "fieldtype": "Link",
            "options": "Task",
            "hidden": 1,
            "read_only": 1
        })
        print("Added task_link field")
    with open(file_path, "w") as f:
        json.dump(doc, f, indent=4)
    print("Compliance JSON updated.")
def create_ca_engagement():
    print("Creating CA Engagement DocType...")
    base_path = "apps/ca_practice/ca_practice/ca_practice/doctype/ca_engagement"
    os.makedirs(base_path, exist_ok=True)
    
    doc_json = {
        "name": "CA Engagement",
        "doctype": "DocType",
        "module": "CA Practice",
        "fields": [
            {"fieldname": "client", "label": "Client", "fieldtype": "Link", "options": "CA Client", "reqd": 1},
            {"fieldname": "client_name", "label": "Client Name", "fieldtype": "Data", "read_only": 1},
            {"fieldname": "engagement_partner", "label": "Engagement Partner", "fieldtype": "Link", "options": "User"},
            {"fieldname": "engagement_date", "label": "Engagement Date", "fieldtype": "Date", "default": "Today"},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "Draft\nActive\nCompleted", "default": "Draft"}
        ],
        "permissions": [{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}]
    }
    
    doc_py = """
import frappe
from frappe.model.document import Document
class CAEngagement(Document):
    pass
"""
    with open(f"{base_path}/ca_engagement.json", "w") as f:
        json.dump(doc_json, f, indent=4)
        
    with open(f"{base_path}/ca_engagement.py", "w") as f:
        f.write(doc_py)
        
    with open(f"{base_path}/__init__.py", "w") as f:
        f.write("")
        
    print("CA Engagement DocType created.")
def main():
    fix_compliance_json()
    create_ca_engagement()
    print("Fixes applied. Now run 'bench migrate' to update the database.")
if __name__ == "__main__":
    main()
