{
    "name": "Import Product from Ecommerce - Tokopedia",
    "summary": "Import products from Tokopedia",
    "description": """
        Extends the base Import Product from Ecommerce module to scrape and import products from Tokopedia.
    """,
    "author": "Alle Aldine",
    "website": "https://haiper.id",
    "category": "Sales",
    "version": "1.0",
    "depends": ["import_product_from_ecommerce"],
    "data": [],
    "installable": True,
    "application": False,
    "images": [
        "static/description/cover.png",
    ],
    "license": "LGPL-3",
    "price": 20.00,
    "currency": "EUR",
    "external_dependencies": {
        "python": ["requests", "beautifulsoup4"],
    },
}
