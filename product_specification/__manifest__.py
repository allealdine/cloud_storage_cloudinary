# -*- coding: utf-8 -*-
{
    "name": "Product Specification",
    "version": "18.0.1.0.0",
    "category": "Product",
    "sequence": 1,
    "summary": "Manage detailed product specifications in Odoo",
    "complexity": "easy",
    "description": """
        Enhance your Odoo product management with Product Specification. This module allows you to define and manage
        detailed specifications for your products, such as technical details, custom attributes, or categorized features.
        Ideal for manufacturers, retailers, or any business needing to provide precise product information.

        Key Features:
        - Add custom specification fields to product templates.
        - Organize specs into categories and line items.
        - Seamless integration with Odoo’s product module.
        - User-friendly interface for easy setup and management.
    """,
    "author": "Alle Aldine",
    "website": "https://haiper.id",
    "depends": [
        "product",
    ],
    "data": [
        "security/specification_security.xml",
        "security/ir.model.access.csv",
        "views/product_template_view.xml",
        "views/product_spec_view.xml",
        "views/product_spec_line_view.xml",
        "views/product_spec_value_view.xml",
        "views/product_spec_category_view.xml",
    ],
    "images": [
        "static/description/cover.png",
    ],
    "installable": True,
    "license": "LGPL-3",
    "price": 25.00,
    "currency": "EUR",
}
