{
    "name": "BinaryGuard Dispatch Management",
    "version": "19.0.1.0.0",
    "summary": "Technician dispatch, scheduling and field-job coordination",
    "description": """
BinaryGuard Dispatch Management
===============================

Coordinates technician assignments, emergency calls, site visits,
installations, maintenance visits and other security-service jobs.

Dispatch records can be linked to service requests, helpdesk tickets,
maintenance plans, projects, field-service tasks, contracts and assets.
    """,
    "author": "BinaryGuard Innovations Inc.",
    "website": "https://binaryguard.ca",
    "category": "Services/Dispatch",
    "license": "LGPL-3",
    "depends": [
        "mail",
        "project",
        "binaryguard_core",
        "binaryguard_service_requests",
        "binaryguard_helpdesk",
        "binaryguard_maintenance",
        "binaryguard_projects",
        "binaryguard_field_service",
        "binaryguard_assets",
        "binaryguard_contracts",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/dispatch_sequence.xml",
        "views/dispatch_views.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
