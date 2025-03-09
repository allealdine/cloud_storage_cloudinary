# -*- coding: utf-8 -*-
{
    "name": "Website Product Specification",
    "version": "18.0.1.0.0",  # Updated to match Odoo 18
    "category": "Website",
    "summary": "Display product specifications on your Odoo website",
    "description": """
        Extend your Odoo website with Website Product Specification. This module integrates with the
        'product_specification' module to showcase detailed product specifications on your website’s
        product pages. Enhance your e-commerce experience by providing customers with clear, structured
        product information directly on your online store.

        Key Features:
        - Display product specifications from 'product_specification' on website product pages.
        - Seamless integration with Odoo’s Website Sale module.
        - Free add-on to enhance the paid 'product_specification' module.
        - Easy setup with no additional configuration needed beyond 'product_specification'.

        Note: This module is free but requires the paid 'product_specification' module to function.
    """,
    "author": "Alle Aldine",
    "website": "https://haiper.id",
    "depends": [
        "website_sale",  # For website product pages
        "product_specification",  # Paid dependency
    ],
    "data": [
        "views/templates.xml",
    ],
    "images": [
        "static/description/cover.png",
    ],
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
    "price": 0.00,  # Free module
    "currency": "EUR",
}
