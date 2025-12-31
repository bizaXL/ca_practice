# ca_practice/ca_practice/utils.py

import frappe
from frappe.utils import getdate, today, add_days, now_datetime, format_date
from frappe import _
import json

def send_daily_reminders():
    """Send daily reminders for compliances due in next 7 days"""
    
    # Get compliances due in next 7 days
    due_compliances = frappe.db.sql("""
        SELECT 
            c.name, c.client, c.client_name, c.compliance_type,
            c.due_date, c.responsible_person, c.status
        FROM `tabCompliance` c
        WHERE 
            c.status IN ('Pending', 'In Progress')
            AND c.due_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
            AND c.docstatus = 0
    """, as_dict=1)
    
    for compliance in due_compliances:
        # Get responsible person's email
        user_email = frappe.db.get_value("User", compliance.responsible_person, "email")
        
        if user_email:
            days_remaining = (getdate(compliance.due_date) - getdate(today())).days
            
            subject = f"Reminder: {compliance.compliance_type} due in {days_remaining} days"
            message = f"""
            <p>Dear {compliance.responsible_person},</p>
            
            <p>This is a reminder for the following compliance:</p>
            
            <table border="0" cellpadding="5" cellspacing="0">
                <tr><td><b>Client:</b></td><td>{compliance.client_name}</td></tr>
                <tr><td><b>Compliance Type:</b></td><td>{compliance.compliance_type}</td></tr>
                <tr><td><b>Due Date:</b></td><td>{format_date(compliance.due_date)}</td></tr>
                <tr><td><b>Days Remaining:</b></td><td>{days_remaining}</td></tr>
                <tr><td><b>Status:</b></td><td>{compliance.status}</td></tr>
            </table>
            
            <p>Please ensure timely completion.</p>
            
            <p>Regards,<br>
            System Notification</p>
            """
            
            frappe.sendmail(
                recipients=[user_email],
                subject=subject,
                message=message,
                reference_doctype="Compliance",
                reference_name=compliance.name
            )
            
            # Update last reminder date
            frappe.db.set_value("Compliance", compliance.name, "last_reminder_date", today())
            frappe.db.set_value("Compliance", compliance.name, "reminder_sent", 1)

def create_monthly_compliances():
    """Create monthly recurring compliances"""
    
    # Get all clients with GST monthly filing
    clients = frappe.db.sql("""
        SELECT name, client_name, gst_filing_frequency
        FROM `tabCA Client`
        WHERE gst_filing_frequency = 'Monthly'
    """, as_dict=1)
    
    for client in clients:
        # Create GST compliances for next 3 months
        for i in range(1, 4):
            due_date = add_days(getdate(today()), 30 * i)
            period = due_date.strftime("%B %Y")
            
            # GSTR-1
            frappe.get_doc({
                "doctype": "Compliance",
                "client": client.name,
                "client_name": client.client_name,
                "compliance_type": "GSTR-1",
                "description": f"GSTR-1 filing for {period}",
                "period": period,
                "due_date": add_days(due_date, 10),  # Usually 10th of next month
                "status": "Pending"
            }).insert()
            
            # GSTR-3B
            frappe.get_doc({
                "doctype": "Compliance",
                "client": client.name,
                "client_name": client.client_name,
                "compliance_type": "GSTR-3B",
                "description": f"GSTR-3B filing for {period}",
                "period": period,
                "due_date": add_days(due_date, 20),  # Usually 20th of next month
                "status": "Pending"
            }).insert()

def update_compliance_status():
    """Update status of compliances based on due date"""
    
    # Update overdue compliances
    frappe.db.sql("""
        UPDATE `tabCompliance`
        SET status = 'Overdue'
        WHERE status IN ('Pending', 'In Progress')
        AND due_date < CURDATE()
        AND (extended_due_date IS NULL OR extended_due_date < CURDATE())
        AND actual_submission_date IS NULL
    """)
    
    # Update 'Due Soon' status (7 days before due)
    frappe.db.sql("""
        UPDATE `tabCompliance`
        SET status = 'In Progress'
        WHERE status = 'Pending'
        AND due_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
        AND actual_submission_date IS NULL
    """)

def send_weekly_summary():
    """Send weekly compliance summary to partners"""
    
    # Get all partners
    partners = frappe.db.sql("""
        SELECT name, email
        FROM `tabUser`
        WHERE enabled = 1
        AND name IN (
            SELECT parent FROM `tabHas Role`
            WHERE role = 'System Manager'
        )
    """, as_dict=1)
    
    # Get compliance summary
    summary = frappe.db.sql("""
        SELECT 
            status,
            COUNT(*) as count
        FROM `tabCompliance`
        WHERE docstatus = 0
        GROUP BY status
    """, as_dict=1)
    
    overdue_compliances = frappe.db.sql("""
        SELECT 
            client_name,
            compliance_type,
            due_date,
            DATEDIFF(CURDATE(), due_date) as days_overdue
        FROM `tabCompliance`
        WHERE status = 'Overdue'
        ORDER BY due_date
        LIMIT 10
    """, as_dict=1)
    
    for partner in partners:
        subject = "Weekly Compliance Summary"
        
        summary_html = "<h3>Compliance Summary</h3><table border='1' cellpadding='5'>"
        for item in summary:
            summary_html += f"<tr><td>{item.status}</td><td>{item.count}</td></tr>"
        summary_html += "</table>"
        
        overdue_html = "<h3>Top 10 Overdue Compliances</h3><table border='1' cellpadding='5'><tr><th>Client</th><th>Type</th><th>Due Date</th><th>Days Overdue</th></tr>"
        for comp in overdue_compliances:
            overdue_html += f"<tr><td>{comp.client_name}</td><td>{comp.compliance_type}</td><td>{format_date(comp.due_date)}</td><td>{comp.days_overdue}</td></tr>"
        overdue_html += "</table>"
        
        message = f"""
        <p>Dear {partner.name},</p>
        
        <p>Here is your weekly compliance summary:</p>
        
        {summary_html}
        
        {overdue_html if overdue_compliances else ''}
        
        <p>Regards,<br>
        CA Practice System</p>
        """
        
        frappe.sendmail(
            recipients=[partner.email],
            subject=subject,
            message=message
        )
