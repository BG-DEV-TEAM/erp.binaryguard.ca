{
    "name": "BinaryGuard Client Portal",
    "version": "19.0.1.0.0",
    "summary": "Customer portal for BinaryGuard operational records",
    "description": """
BinaryGuard Client Portal
=========================

Allows authenticated customer portal users to view their BinaryGuard
assets, service contracts, support tickets, access cards and preventive
maintenance plans.
    """,
    "author": "BinaryGuard Innovations Inc.",
    "website": "https://binaryguard.ca",
    "category": "Website/Portal",
    "license": "LGPL-3",
    "depends": [
        "portal",
        "website",
        "binaryguard_assets",
        "binaryguard_contracts",
        "binaryguard_helpdesk",
        "binaryguard_access_cards",
        "binaryguard_maintenance",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/portal_rules.xml",
        "views/portal_templates.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
