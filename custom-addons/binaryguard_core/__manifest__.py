{
    "name": "BinaryGuard Core",
    "version": "19.0.1.0.0",
    "summary": "Core data and configuration for BinaryGuard ERP",
    "description": """
BinaryGuard Core
================

Provides the foundation models, menus and configuration used by
BinaryGuard custom ERP modules.
    """,
    "author": "BinaryGuard Innovations Inc.",
    "website": "https://binaryguard.ca",
    "category": "Administration",
    "license": "LGPL-3",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/binaryguard_client_views.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
