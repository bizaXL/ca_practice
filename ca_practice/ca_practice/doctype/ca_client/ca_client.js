frappe.ui.form.on('CA Client', {
    refresh: function(frm) {
        // Add custom buttons
        frm.add_custom_button(__('Create Engagement'), function() {
            frappe.model.open_mapped_doc({
                method: "ca_practice.ca_practice.doctype.ca_client.ca_client.create_engagement",
                frm: frm
            });
        }, __("Actions"));
        
        frm.add_custom_button(__('View Compliances'), function() {
            frappe.set_route('List', 'Compliance', {'client': frm.doc.name});
        }, __("Actions"));
        
        frm.add_custom_button(__('Service Status Report'), function() {
            frappe.set_route('query-report', 'Client Service Status', {'client': frm.doc.name});
        }, __("Reports"));
    },
    
    customer: function(frm) {
        if (frm.doc.customer) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Customer",
                    name: frm.doc.customer
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value("client_name", r.message.customer_name);
                        // Auto-generate client code
                        if (!frm.doc.client_code) {
                            var code = "CL" + frm.doc.customer.slice(-4) + new Date().getFullYear().toString().slice(-2);
                            frm.set_value("client_code", code);
                        }
                    }
                }
            });
        }
    },
    
    validate: function(frm) {
        // Validate PAN format
        if (frm.doc.pan_number) {
            var pan_regex = /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/;
            if (!pan_regex.test(frm.doc.pan_number)) {
                frappe.msgprint(__("PAN number format is invalid. Format: ABCDE1234F"));
                frappe.validated = false;
            }
        }
        
        // Validate GSTIN format if provided
        if (frm.doc.gstin) {
            var gst_regex = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/;
            if (!gst_regex.test(frm.doc.gstin)) {
                frappe.msgprint(__("GSTIN format is invalid"));
                frappe.validated = false;
            }
        }
    }
});
