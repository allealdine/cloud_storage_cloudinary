# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re
from odoo import models
from odoo.exceptions import ValidationError
from ..utils.cloud_storage_cloudinary_utils import (
    generate_cloudinary_upload_url,
    get_cloudinary_resource_url,
)


class IrAttachment(models.Model):
    _inherit = "ir.attachment"
    _cloud_storage_cloudinary_url_pattern = r"https?://res.cloudinary.com/(?P<cloud_name>[^/]+)/raw/upload/(?P<public_id>.+)"

    def _get_cloud_storage_cloudinary_info(self):
        match = re.match(self._cloud_storage_cloudinary_url_pattern, self.url)
        if not match:
            raise ValidationError(f"{self.url} is not a valid Cloudinary URL.")
        return {
            "cloud_name": match.group("cloud_name"),
            "public_id": match.group("public_id"),
        }

    def _generate_cloud_storage_cloudinary_url(self, public_id):
        cloud_name = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("cloud_storage_cloudinary_cloud_name")
        )
        return f"https://res.cloudinary.com/{cloud_name}/raw/upload/{public_id}"

    def _generate_cloud_storage_cloudinary_signed_url(self, public_id, **kwargs):
        return generate_cloudinary_upload_url(
            self.env,
            public_id,
            method=kwargs.get("method", "GET"),
            expiration=kwargs.get("expiration", 3600),
        )

    def _generate_cloud_storage_url(self):
        if (
            self.env["ir.config_parameter"].sudo().get_param("cloud_storage_provider")
            != "cloudinary"
        ):
            return super()._generate_cloud_storage_url()
        public_id = (
            self._generate_cloud_storage_blob_name()
        )  # Assumes this method exists in parent
        return self._generate_cloud_storage_cloudinary_url(public_id)

    def _generate_cloud_storage_download_info(self):
        if (
            self.env["ir.config_parameter"].sudo().get_param("cloud_storage_provider")
            != "cloudinary"
        ):
            return super()._generate_cloud_storage_download_info()
        info = self._get_cloud_storage_cloudinary_info()
        return {
            "url": get_cloudinary_resource_url(self.env, info["public_id"]),
            "time_to_expiry": self._cloud_storage_download_url_time_to_expiry,
        }

    def _generate_cloud_storage_upload_info(self):
        if (
            self.env["ir.config_parameter"].sudo().get_param("cloud_storage_provider")
            != "cloudinary"
        ):
            return super()._generate_cloud_storage_upload_info()
        info = self._get_cloud_storage_cloudinary_info()
        return {
            "url": self._generate_cloud_storage_cloudinary_signed_url(
                info["public_id"], method="PUT"
            ),
            "method": "PUT",
            "response_status": 200,
        }
