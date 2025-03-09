# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Cloud Storage Cloudinary",
    "summary": "Store chatter attachments in Cloudinary",
    "description": """
        Seamlessly integrate Odoo with Cloudinary to store and manage chatter attachments in the cloud.
        This module extends the 'cloud_storage' framework to offload files to Cloudinary, offering scalable,
        secure storage for your Odoo attachments. Perfect for businesses handling images, PDFs, and other
        documents in chatter.

        Key Features:
        - Upload attachments directly to Cloudinary from Odoo chatter.
        - Securely store files with signed URLs.
        - Easy configuration via Odoo settings.
        - Requires the 'cloud_storage' base module.

        Ideal for e-commerce, marketing, or any Odoo user needing efficient cloud storage.
    """,
    "author": "Alle Aldine",
    "website": "https://haiper.id",
    "category": "Technical Settings",
    "version": "18.0.1.0.0",
    "depends": ["cloud_storage"],
    "external_dependencies": {"python": ["cloudinary"]},
    "data": [
        "views/settings.xml",
    ],
    "images": [
        "static/description/icon.png",
        "static/description/screenshot1.png",
    ],
    "license": "LGPL-3",
    "price": 99.00,
    "currency": "EUR",
    "application": False,
    "installable": True,
    "auto_install": False,
}
