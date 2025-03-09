# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


class ProductSpecificationCategory(models.Model):
    _name = "product.spec.category"
    _description = "Product Specification Category"

    name = fields.Char("Category Name", required=True, translate=True)
    sequence = fields.Integer(
        "Sequence", help="Determine the display order", index=True, default=10
    )
    description = fields.Html()


class ProductSpecification(models.Model):
    _name = "product.spec"
    _description = "Product Specification"
    _order = "sequence, id"

    name = fields.Char("Specification", required=True, translate=True)
    categ_id = fields.Many2one("product.spec.category", string="Specification Category")
    sequence = fields.Integer(
        "Sequence", help="Determine the display order", index=True, default=10
    )
    spec_line_ids = fields.One2many("product.spec.line", "spec_id", "Lines")
    is_used_on_products = fields.Boolean(
        "Used on Products", compute="_compute_is_used_on_products"
    )
    product_tmpl_ids = fields.Many2many(
        "product.template",
        string="Related Product Templates",
        compute="_compute_products",
        store=True,
    )
    product_ids = fields.Many2many(
        "product.product",
        string="Related Products",
        compute="_compute_products",
        store=True,
    )
    product_categories = fields.Many2many(
        "product.category",
        "product_category_spec_rel",
        "categ_id",
        "spec_id",
        string="Categories",
    )
    value_ids = fields.One2many("product.spec.value", "spec_id", "Values", copy=True)
    note = fields.Text(string="Description")

    @api.depends("product_ids")
    def _compute_is_used_on_products(self):
        for pa in self:
            pa.is_used_on_products = bool(pa.product_ids)

    @api.depends("spec_line_ids.active", "spec_line_ids.product_id")
    def _compute_products(self):
        for pa in self:
            pa.product_tmpl_ids = pa.spec_line_ids.product_tmpl_id
            pa.product_ids = pa.spec_line_ids.product_id

    def write(self, vals):
        invalidate_cache = "sequence" in vals and any(
            record.sequence != vals["sequence"] for record in self
        )
        res = super(ProductSpecification, self).write(vals)
        if invalidate_cache:
            self.flush()
            self.invalidate_cache()
        return res

    def unlink(self):
        for pa in self:
            if pa.is_used_on_products:
                raise UserError(
                    _(
                        "You cannot delete the spec %s because it is used on the following products:\n%s"
                    )
                    % (
                        pa.display_name,
                        ", ".join(pa.product_ids.mapped("display_name")),
                    )
                )
        return super(ProductSpecification, self).unlink()

    def action_read_spec(self):
        self.ensure_one()
        return {
            "name": self.display_name,
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "product.spec",
            "res_id": self.id,
        }


class ProductProductSpecLine(models.Model):
    _name = "product.spec.line"
    _rec_name = "spec_id"
    _description = "Product Spec Line"
    _order = "categ_id, sequence, spec_id, value_sequence, id"

    active = fields.Boolean(default=True)
    product_tmpl_id = fields.Many2one(
        "product.template",
        string="Product Template",
        ondelete="cascade",
        required=False,
        index=True,
    )
    product_variant_ids = fields.Many2many(
        'product.product', 
        string="Product Variants",
        help="Select Variants of the Product for which this rule applies. Leave empty if this rule applies for any variant of this template.")
    product_categ_id = fields.Many2one(
        "product.category",
        string="Product Category",
        related="product_tmpl_id.categ_id",
    )
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        ondelete="cascade",
        required=True,
        index=True,
    )
    spec_id = fields.Many2one(
        "product.spec",
        string="Specification",
        ondelete="restrict",
        required=True,
        index=True,
    )
    categ_id = fields.Many2one(
        "product.spec.category",
        related="spec_id.categ_id",
        string="Specification Category",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence", help="Determine the display order", index=True, default=1
    )
    value_sequence = fields.Integer(related='value_id.sequence', store=True, string='Value Sequence')
    value_id = fields.Many2one(
        "product.spec.value",
        string="Value",
        domain="[('spec_id', '=', spec_id)]",
        ondelete="restrict",
        required=True,
    )
    note = fields.Text(related="spec_id.note")

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get("product_tmpl_id") and not val.get("product_id"):
                product_tmpl_id = self.env["product.template"].browse(
                    val.get("product_tmpl_id")
                )
                val["product_id"] = product_tmpl_id.product_variant_id.id
        return super(ProductProductSpecLine, self).create(vals_list)

    _sql_constraints = []

    @api.constrains('product_variant_ids', 'spec_id')
    def _check_unique_spec_per_variant(self):
        for record in self:
            if record.product_variant_ids:
                for variant in record.product_variant_ids:
                    existing_line = self.search([
                        ('spec_id', '=', record.spec_id.id),
                        ('product_variant_ids', 'in', [variant.id]),
                        ('id', '!=', record.id)
                    ])
                    if existing_line:
                        raise ValidationError(
                            'The specification {} already exists for the variant {}!'.format(
                                record.spec_id.name, variant.display_name
                            )
                        )

class ProductSpecValue(models.Model):
    _name = "product.spec.value"

    _order = "spec_id, sequence, id"
    _description = "Attribute Value"

    name = fields.Char(string="Value", required=True, translate=True)
    sequence = fields.Integer(
        string="Sequence", help="Determine the display order", index=True, default=1
    )
    spec_id = fields.Many2one(
        "product.spec",
        string="Specification",
        ondelete="cascade",
        required=True,
        index=True,
        help="The attribute cannot be changed once the value is used on at least one product.",
    )

    _sql_constraints = [
        (
            "value_spec_uniq",
            "unique (name, spec_id)",
            "You cannot create two values with the same name for the same specification.",
        )
    ]
