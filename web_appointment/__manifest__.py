{
    "name": "Web Appointment",
    "version": "1.0",
    "category": "Website",
    "summary": "Client can book appointment from website",
    "depends": [
        "website",
        "hr",
        "project",
        "calendar",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/website_appointment_views.xml",
        "views/templates.xml",
        "views/availability_views.xml",
        "views/view_project_views.xml",
    ],
    # 💰 SELLING INFO
    "price": 400.00,
    "currency": "EUR",
    "installable": True,
}