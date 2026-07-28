{
    "name": "BinaryGuard Service Requests",
    "version": "19.0.1.0.0",
    "summary": "Customer service requests, triage and technician assignment",
    "description": """
BinaryGuard Service Requests
============================

Central service-request workflow for technical support, site visits,
installations, CCTV, access control, networking and emergency service.
    """,
    "author": "BinaryGuard Innovations Inc.",
    "website": "https://binaryguard.ca",
    "category": "Services/Service Requests",
    "license": "LGPL-3",
    "depends": [
        "mail",
        "project",
        "binaryguard_core",
        "binaryguard_assets",
        "binaryguard_contracts",
        "binaryguard_helpdesk",
        "binaryguard_field_service",
        "binaryguard_portal",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/service_request_sequence.xml",
        "views/service_request_views.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
