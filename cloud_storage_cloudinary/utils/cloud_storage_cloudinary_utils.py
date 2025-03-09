# Part of Odoo. See LICENSE file for full copyright and licensing details.

import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url, api_sign_request
import time


def configure_cloudinary(env):
    config = {
        "cloud_name": env["ir.config_parameter"]
        .sudo()
        .get_param("cloud_storage_cloudinary_cloud_name"),
        "api_key": env["ir.config_parameter"]
        .sudo()
        .get_param("cloud_storage_cloudinary_api_key"),
        "api_secret": env["ir.config_parameter"]
        .sudo()
        .get_param("cloud_storage_cloudinary_api_secret"),
    }
    cloudinary.config(**config)
    return config


def generate_cloudinary_upload_url(env, public_id, method="POST", expiration=3600):
    config = configure_cloudinary(env)
    timestamp = int(time.time())
    params = {
        "public_id": public_id,
        "timestamp": timestamp,
    }
    signature = api_sign_request(params, config["api_secret"])
    url = f"https://api.cloudinary.com/v1_1/{config['cloud_name']}/raw/upload"
    return f"{url}?public_id={public_id}&timestamp={timestamp}&api_key={config['api_key']}&signature={signature}"


def get_cloudinary_resource_url(env, public_id):
    configure_cloudinary(env)
    url, _ = cloudinary.utils.cloudinary_url(public_id, resource_type="raw")
    return url
