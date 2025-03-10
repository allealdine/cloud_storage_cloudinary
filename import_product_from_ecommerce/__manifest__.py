{
    "name": "Import Product from Ecommerce (Base)",
    "summary": "Base module for importing products from ecommerce platforms",
    "description": """
        Provides the base structure for importing products from various ecommerce sources.
        Other modules can extend this to add specific platform support (e.g., Tokopedia, Shopee).
    """,
    "author": "Alle Aldine",
    "website": "https://haiper.id",
    "category": "Sales",
    "version": "1.0",
    "depends": ["sale"],
    "data": [
        "security/ir.model.access.csv",
        "wizards/import_product_views.xml",
    ],
    "installable": True,
    "application": False,
    "images": [
        "static/description/cover.png",
    ],
    "license": "LGPL-3",
    "price": 70.00,
    "currency": "EUR",
}
