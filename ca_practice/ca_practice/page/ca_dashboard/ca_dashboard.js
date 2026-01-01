frappe.pages['ca-dashboard'].on_page_load = function (wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'CA Dashboard',
        single_column: true
    });
    page.main.html("<div style='padding: 20px;'><h3>Welcome to CA Practice Dashboard</h3><p>Use the workspace to see metrics.</p></div>");
}
