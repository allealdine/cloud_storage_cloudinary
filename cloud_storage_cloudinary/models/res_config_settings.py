# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import requests
from ..utils.cloud_storage_cloudinary_utils import generate_cloudinary_upload_url


class CloudStorageSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cloud_storage_provider = fields.Selection(
        selection_add=[("cloudinary", "Cloudinary")]
    )
    cloud_storage_cloudinary_cloud_name = fields.Char(
        string="Cloudinary Cloud Name",
        config_parameter="cloud_storage_cloudinary_cloud_name",
    )
    cloud_storage_cloudinary_api_key = fields.Char(
        string="Cloudinary API Key",
        config_parameter="cloud_storage_cloudinary_api_key",
    )
    cloud_storage_cloudinary_api_secret = fields.Char(
        string="Cloudinary API Secret",
        config_parameter="cloud_storage_cloudinary_api_secret",
    )

    def _setup_cloud_storage_provider(self):
        if (
            self.env["ir.config_parameter"].sudo().get_param("cloud_storage_provider")
            != "cloudinary"
        ):
            return super()._setup_cloud_storage_provider()
        cloud_name = self.cloud_storage_cloudinary_cloud_name
        api_key = self.cloud_storage_cloudinary_api_key
        api_secret = self.cloud_storage_cloudinary_api_secret
        if not all([cloud_name, api_key, api_secret]):
            raise ValidationError(_("Cloudinary configuration is incomplete."))
        test_public_id = f"odoo_test_{self.env.cr.dbname}"
        upload_url = generate_cloudinary_upload_url(
            self.env, test_public_id, method="POST"
        )
        response = requests.post(
            upload_url, files={"file": ("test.txt", b"test")}, timeout=5
        )
        if response.status_code != 200:
            raise ValidationError(
                _("Failed to upload to Cloudinary: %s", response.text)
            )

    def _get_cloud_storage_configuration(self):
        ICP = self.env["ir.config_parameter"].sudo()
        if ICP.get_param("cloud_storage_provider") != "cloudinary":
            return super()._get_cloud_storage_configuration()
        configuration = {
            "cloud_name": ICP.get_param("cloud_storage_cloudinary_cloud_name"),
            "api_key": ICP.get_param("cloud_storage_cloudinary_api_key"),
            "api_secret": ICP.get_param("cloud_storage_cloudinary_api_secret"),
        }
        return configuration if all(configuration.values()) else {}
