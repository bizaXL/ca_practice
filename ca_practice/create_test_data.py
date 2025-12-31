import frappe
from frappe.utils import add_days, nowdate

def create_test_clients():
    """Create sample clients for testing"""
    
    clients = [
        {
            "client_code": "CL001",
            "client_name": "ABC Enterprises",
            "client_type": "Private Limited",
            "pan_number": "ABCPS1234D",
            "gstin": "27ABCPS1234D1Z5",
            "financial_year_end": "2024-03-31",
            "engagement_partner": "Administrator"
        },
        {
            "client_code": "CL002", 
            "client_name": "XYZ Traders",
            "client_type": "Proprietorship",
            "pan_number": "XYZPS5678E",
            "gstin": "27XYZPS5678E1Z6",
            "financial_year_end": "2024-03-31",
            "engagement_partner": "Administrator"
        }
    ]
    
    for client_data in clients:
        # 1. Check if Customer exists, if not create it
        if not frappe.db.exists("Customer", client_data["client_name"]):
            customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": client_data["client_name"],
                "customer_type": "Company",
                "customer_group": "Commercial",
                "territory": "India"
            })
            customer.insert()
            print(f"Created Customer: {client_data['client_name']}")
        
        # 2. Create CA Client linked to that Customer
        if not frappe.db.exists("CA Client", {"client_code": client_data["client_code"]}):
            client = frappe.get_doc({
                "doctype": "CA Client",
                "customer": client_data["client_name"], # Linked Customer
                **client_data
            })
            client.insert()
            print(f"Created CA Client: {client.client_name}")

def create_test_compliances():
    """Create sample compliances"""
    
    clients = frappe.get_all("CA Client", fields=["name", "client_name"])
    
    if not clients:
        print("No clients found. Please create clients first.")
        return

    compliance_types = [
        ("GSTR-1", "Monthly", 10),
        ("GSTR-3B", "Monthly", 20),
        ("Income Tax Return", "Yearly", 150),
        ("TDS Return (24Q)", "Quarterly", 30)
    ]
    
    for client in clients:
        for comp_type, frequency, days_to_add in compliance_types:
            frappe.get_doc({
                "doctype": "Compliance",
                "client": client.name,
                "client_name": client.client_name,
                "compliance_type": comp_type,
                "description": f"Test {comp_type} for {client.client_name}",
                "period": "Test Period",
                "due_date": add_days(nowdate(), days_to_add),
                "status": "Pending",
                "responsible_person": "Administrator"
            }).insert()
    
    print("Created test compliances")

def main():
    create_test_clients()
    create_test_compliances()
    frappe.db.commit()
    print("Test data created successfully.")

if __name__ == "__main__":
    frappe.connect()
    main()
