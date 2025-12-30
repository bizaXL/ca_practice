import frappe
from frappe.utils import nowdate, add_days
from frappe import _

def create_test_clients():
    """Create sample clients for testing"""
    
    print("Creating test clients...")
    
    # Check if test clients already exist
    if frappe.db.exists("CA Client", "CL001"):
        print("Test clients already exist. Skipping...")
        return
    
    clients = [
        {
            "client_code": "CL001",
            "client_name": "ABC Enterprises Pvt. Ltd.",
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
        },
        {
            "client_code": "CL003",
            "client_name": "Global Services LLP",
            "client_type": "LLP",
            "pan_number": "GLOBLLP9012F",
            "financial_year_end": "2024-03-31",
            "engagement_partner": "Administrator"
        }
    ]
    
    created_clients = []
    for client_data in clients:
        try:
            # Create customer first
            customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": client_data["client_name"],
                "customer_type": "Company",
                "territory": "India"
            })
            customer.insert()
            
            # Create CA Client
            client = frappe.get_doc({
                "doctype": "CA Client",
                "customer": customer.name,
                **client_data
            })
            client.insert()
            created_clients.append(client.name)
            print(f"Created client: {client.client_name} ({client.client_code})")
            
        except Exception as e:
            print(f"Error creating client {client_data['client_name']}: {str(e)}")
    
    frappe.db.commit()
    print(f"\nCreated {len(created_clients)} test clients")
    return created_clients

def create_test_compliances():
    """Create sample compliances"""
    
    print("\nCreating test compliances...")
    
    # Get all clients
    clients = frappe.get_all("CA Client", fields=["name", "client_name"])
    
    if not clients:
        print("No clients found. Create clients first.")
        return
    
    compliance_types = [
        ("GSTR-1", "Monthly", 10),
        ("GSTR-3B", "Monthly", 20),
        ("Income Tax Return", "Yearly", 150),
        ("TDS Return (24Q)", "Quarterly", 30),
        ("ROC Form AOC-4", "Yearly", 180)
    ]
    
    created_compliances = 0
    for client in clients:
        for comp_type, frequency, days_to_add in compliance_types:
            try:
                compliance = frappe.get_doc({
                    "doctype": "Compliance",
                    "client": client.name,
                    "client_name": client.client_name,
                    "compliance_type": comp_type,
                    "description": f"{comp_type} filing for {client.client_name}",
                    "period": f"Test Period - {frequency}",
                    "due_date": add_days(nowdate(), days_to_add),
                    "status": "Pending",
                    "responsible_person": "Administrator"
                })
                compliance.insert()
                created_compliances += 1
                
            except Exception as e:
                print(f"Error creating compliance for {client.client_name}: {str(e)}")
    
    frappe.db.commit()
    print(f"Created {created_compliances} test compliances")
    return created_compliances

def main():
    """Main function to create test data"""
    print("=" * 50)
    print("Creating Test Data for CA Practice")
    print("=" * 50)
    
    # Create test clients
    clients = create_test_clients()
    
    # Create test compliances
    if clients:
        compliances = create_test_compliances()
    
    print("\n" + "=" * 50)
    print("Test Data Creation Complete!")
    print("=" * 50)
    
    # Show summary
    client_count = frappe.db.count("CA Client")
    compliance_count = frappe.db.count("Compliance")
    
    print(f"\nSummary:")
    print(f"  Total Clients: {client_count}")
    print(f"  Total Compliances: {compliance_count}")
    print(f"\nYou can now access:")
    print(f"  1. CA Client list: http://localhost:8000/app/ca-client")
    print(f"  2. Compliance list: http://localhost:8000/app/compliance")

if __name__ == "__main__":
    main()
