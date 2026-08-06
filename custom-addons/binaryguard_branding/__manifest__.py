{
    "name": "BinaryGuard Branding",
    "version": "19.0.1.0.0",
    "summary": "BinaryGuard ERP branding and interface customization",
    "description": """
Provides BinaryGuard ERP branding, theme colours,
browser title, login page styling and interface customization.
""",
    "author": "BinaryGuard Innovations Inc.",
    "website": "https://binaryguard.ca",
    "category": "BinaryGuard/Administration",
    "license": "LGPL-3",
    "depends": [
        "web",
        "website",
    ],
    "data": [
        "views/website_branding.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "binaryguard_branding/static/src/scss/backend.scss",
            "binaryguard_branding/static/src/js/title_service.js",
        ],
        "web.assets_frontend": [
            "binaryguard_branding/static/src/scss/login.scss",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
