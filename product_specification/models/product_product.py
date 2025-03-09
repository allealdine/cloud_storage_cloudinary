# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    spec_line_ids = fields.One2many(
        "product.spec.line", "product_tmpl_id", "Product Specification", copy=True
    )


class ProductProduct(models.Model):
    _inherit = "product.product"

    spec_line_ids = fields.One2many(
        "product.spec.line", "product_id", "Product Specification", copy=True
    )
