{
    "name": "BinaryGuard Field Service",
    "version": "19.0.1.0.0",
    "summary": "BinaryGuard Technician Work Orders",
    "author": "BinaryGuard Innovations Inc.",
    "website": "https://binaryguard.ca",
    "license": "LGPL-3",

    "depends": [
        "project",
        "binaryguard_projects",
        "binaryguard_sales",
        "binaryguard_inventory",
    ],

    "data": [
        "views/project_task_views.xml",
    ],

    "installable": True,
    "application": True,
}
