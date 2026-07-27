{
    "name": "BinaryGuard Helpdesk",
    "version": "19.0.1.0.0",
    "summary": "Technical support and service ticket management",
    "description": """
BinaryGuard Helpdesk
====================

Provides customer-support tickets, technical assignments, equipment
references, service status, diagnosis, resolution and follow-up tracking.
    """,
    "author": "BinaryGuard Innovations Inc.",
    "website": "https://binaryguard.ca",
    "category": "Services/Helpdesk",
    "license": "LGPL-3",
    "depends": [
        "mail",
        "project",
        "stock",
        "binaryguard_core",
        "binaryguard_crm",
        "binaryguard_inventory",
        "binaryguard_projects",
        "binaryguard_field_service",
    ],
    "data": [
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",
        "data/helpdesk_sequence.xml",
        "views/helpdesk_ticket_views.xml",
        "views/helpdesk_menus.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
