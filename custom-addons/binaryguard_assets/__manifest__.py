{
    "name": "BinaryGuard Asset Management",
    "version": "19.0.1.0.0",
    "summary": "Customer and company equipment asset register",
    "description": """
BinaryGuard Asset Management
============================

Tracks customer-owned and company-owned security and IT equipment,
including installation details, warranty, lifecycle status, serial
numbers, assigned technicians, related projects and service history.
    """,
    "author": "BinaryGuard Innovations Inc.",
    "website": "https://binaryguard.ca",
    "category": "Operations/Assets",
    "license": "LGPL-3",
    "depends": [
        "mail",
        "product",
        "stock",
        "project",
        "hr",
        "binaryguard_core",
        "binaryguard_inventory",
        "binaryguard_projects",
        "binaryguard_field_service",
        "binaryguard_helpdesk",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/asset_sequence.xml",
        "views/asset_views.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
