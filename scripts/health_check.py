# health_check.py
import frappe
from frappe.utils import now_datetime

def check_system_health():
    issues = []
    
    # Check overdue compliances
    overdue_count = frappe.db.count("Compliance", {
        "status": "Overdue",
        "docstatus": 0
    })
    
    if overdue_count > 10:
        issues.append(f"High number of overdue compliances: {overdue_count}")
    
    # Check pending tasks
    pending_tasks = frappe.db.count("Task", {
        "status": ["in", ["Open", "Working", "Pending Review"]]
    })
    
    if pending_tasks > 50:
        issues.append(f"High number of pending tasks: {pending_tasks}")
    
    # Check scheduler
    last_scheduler_run = frappe.db.get_value("Scheduled Job Log", 
        {"job_name": "ca_practice.ca_practice.utils.send_daily_reminders"},
        "creation", order_by="creation desc")
    
    if last_scheduler_run:
        hours_since_last_run = (now_datetime() - last_scheduler_run).total_seconds() / 3600
        if hours_since_last_run > 24:
            issues.append(f"Daily reminders not run for {hours_since_last_run:.1f} hours")
    
    return issues

def send_health_report():
    issues = check_system_health()
    
    if issues:
        subject = "CA Practice System Health Alert"
        message = "<h3>System Health Issues Detected:</h3><ul>"
        for issue in issues:
            message += f"<li>{issue}</li>"
        message += "</ul><p>Please investigate.</p>"
        
        frappe.sendmail(
            recipients=["admin@example.com"],
            subject=subject,
            message=message
        )
