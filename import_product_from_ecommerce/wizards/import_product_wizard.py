from odoo import models, fields, api
import os


class ImportProductWizard(models.TransientModel):
    _name = "import.product.wizard"
    _description = "Import Product from Ecommerce Wizard"

    source = fields.Selection(
        selection="_get_sources",
        string="Select Source",
        required=True,
        help="Select the ecommerce platform to import products from.",
    )
    source_url = fields.Char(
        string="Source URL",
        help="Enter the URL of the page to scrape products from (e.g., a search or category page).",
    )
    preview_data = fields.Text(
        string="Preview",
        readonly=True,
        help="Preview of the data to be imported from the selected source.",
    )
    temp_file_path = fields.Char(
        string="Temporary File Path",
        readonly=True,
        help="Path to the temporary HTML file storing scraped content.",
    )
    image_html = fields.Html(
        string="Images",
        readonly=True,
        help="Preview of scraped images from the source URL.",
    )

    @api.model
    def _get_sources(self):
        """Dynamic method to be extended by functional modules to add sources."""
        return []

    def action_preview(self):
        """Preview the data from the selected source. To be overridden by functional modules."""
        self.preview_data = (
            "Preview not implemented for this source or no URL provided."
        )
        self.image_html = False  # Reset images
        return {
            "type": "ir.actions.act_window",
            "res_model": "import.product.wizard",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }

    def action_import(self):
        """Import the previewed data. To be overridden by functional modules."""
        return {"type": "ir.actions.act_window_close"}

    def unlink(self):
        """Delete the temporary file when the wizard is closed."""
        for record in self:
            if record.temp_file_path and os.path.exists(record.temp_file_path):
                try:
                    os.unlink(record.temp_file_path)
                except Exception as e:
                    pass
        return super().unlink()
