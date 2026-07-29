{
    "name": "BinaryGuard Branding",
    "version": "19.0.1.0.0",
    "summary": "BinaryGuard ERP branding and interface customization",
    "description": """
        Provides BinaryGuard ERP branding, theme colours,
        browser title, login-page styling and interface customization.
    """,
    "author": "BinaryGuard Innovations Inc.",
    "website": "https://binaryguard.ca",
    "category": "BinaryGuard/Administration",
    "license": "LGPL-3",
    "depends": [
        "web",
    ],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "binaryguard_branding/static/src/scss/backend.scss",
        ],
        "web.assets_frontend": [
            "binaryguard_branding/static/src/scss/login.scss",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}
