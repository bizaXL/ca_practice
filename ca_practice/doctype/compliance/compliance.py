import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today, add_days, format_date
from frappe import _

class Compliance(Document):
    def validate(self):
        self.set_status()
        self.validate_dates()
        
    def before_save(self):
        if not self.task_created and self.status in ["Pending", "In Progress"]:
            self.create_task()
    
    def set_status(self):
        if self.actual_submission_date:
            self.status = "Completed"
        elif self.extended_due_date and getdate(today()) > getdate(self.extended_due_date):
            self.status = "Overdue"
        elif self.due_date and getdate(today()) > getdate(self.due_date):
            self.status = "Overdue"
        elif self.due_date and getdate(add_days(getdate(self.due_date), -7)) <= getdate(today()) <= getdate(self.due_date):
            self.status = "In Progress"
    
    def validate_dates(self):
        if self.actual_submission_date and self.due_date:
            if getdate(self.actual_submission_date) < getdate(self.due_date):
                frappe.msgprint(_("Submission date is before due date. Please verify."), alert=True)
    
    def create_task(self):
        # Create a task for this compliance
        task = frappe.get_doc({
            "doctype": "Task",
            "subject": f"{self.compliance_type} - {self.client_name} ({self.period})",
            "description": self.description,
            "status": "Open",
            "priority": "High" if self.status == "Overdue" else "Medium",
            "due_date": self.extended_due_date or self.due_date,
            "reference_type": "Compliance",
            "reference_name": self.name,
            "assigned_to": self.assigned_to or self.responsible_person
        })
        
        task.insert(ignore_permissions=True)
        self.task_created = 1
        self.task_link = task.name
        
        frappe.msgprint(_("Task {0} created successfully").format(task.name))
    
    def after_insert(self):
        # Send initial notification
        self.send_notification("created")
    
    def on_update(self):
        # Send update notification if status changed
        self.send_notification("updated")
    
    def send_notification(self, action):
        # Get responsible person's email
        user_email = frappe.db.get_value("User", self.responsible_person, "email")
        
        if user_email:
            subject = f"Compliance {action.capitalize()}: {self.compliance_type}"
            message = f"""
            <p>Dear Team,</p>
            
            <p>A compliance has been {action}:</p>
            
            <table border="0" cellpadding="5" cellspacing="0">
                <tr><td><b>Client:</b></td><td>{self.client_name}</td></tr>
                <tr><td><b>Compliance Type:</b></td><td>{self.compliance_type}</td></tr>
                <tr><td><b>Period:</b></td><td>{self.period or 'N/A'}</td></tr>
                <tr><td><b>Due Date:</b></td><td>{format_date(self.due_date)}</td></tr>
                <tr><td><b>Status:</b></td><td>{self.status}</td></tr>
                <tr><td><b>Responsible:</b></td><td>{self.responsible_person}</td></tr>
            </table>
            
            <p>Please take necessary action.</p>
            
            <p>Regards,<br>
            System Notification</p>
            """
            
            frappe.sendmail(
                recipients=[user_email],
                subject=subject,
                message=message,
                reference_doctype=self.doctype,
                reference_name=self.name
            )

@frappe.whitelist()
def create_bulk_compliances(client, compliance_type, start_date, frequency, count):
    """Create multiple compliance records at once"""
    import datetime
    
    start = getdate(start_date)
    compliances_created = []
    
    for i in range(int(count)):
        due_date = start
        
        if frequency == "Monthly":
            due_date = add_days(start, 30 * i)
        elif frequency == "Quarterly":
            due_date = add_days(start, 90 * i)
        elif frequency == "Half Yearly":
            due_date = add_days(start, 180 * i)
        elif frequency == "Yearly":
            due_date = add_days(start, 365 * i)
        
        period = due_date.strftime("%B %Y")
        if frequency == "Quarterly":
            quarter = (due_date.month - 1) // 3 + 1
            period = f"Q{quarter} {due_date.year}"
        elif frequency == "Yearly":
            period = f"FY {due_date.year}-{due_date.year + 1}"
        
        compliance = frappe.get_doc({
            "doctype": "Compliance",
            "client": client,
            "compliance_type": compliance_type,
            "description": f"Auto-generated {compliance_type} for {period}",
            "period": period,
            "due_date": due_date,
            "status": "Pending"
        })
        
        compliance.insert()
        compliances_created.append(compliance.name)
    
    return len(compliances_created)
