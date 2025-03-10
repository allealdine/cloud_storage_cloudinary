import tempfile
import os
import base64
import requests

from odoo import models, fields, api
from bs4 import BeautifulSoup


class ImportProductWizard(models.TransientModel):
    _inherit = "import.product.wizard"

    @api.model
    def _get_sources(self):
        """Add Tokopedia to the source selection."""
        sources = super()._get_sources()
        sources.append(("tokopedia.com", "Tokopedia"))
        return sources

    def _get_image_urls(self, soup):
        image_section = soup.find("div", class_="css-17wadv5")
        image_urls = []
        if image_section:
            images = image_section.select("img.css-1c345mg")
            for img in images:
                if "src" in img.attrs and not img["src"].startswith("data:image"):
                    url = img["src"]
                    if ".jpg" in url or ".png" in url:
                        image_urls.append(url)
        return image_urls

    def _scrape_tokopedia(self):
        """Scrape product data from Tokopedia, including name and images, using a temporary file."""
        if not self.source_url:
            return "Please provide a Tokopedia URL to scrape."

        if self.temp_file_path and os.path.exists(self.temp_file_path):
            with open(self.temp_file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
        else:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                response = requests.get(self.source_url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                zeus_root = soup.find("div", id="zeus-root")
                if not zeus_root:
                    return "No <div id='zeus-root'> found in the provided URL."
                html_content = str(zeus_root)

                temp_file = tempfile.NamedTemporaryFile(
                    delete=False, suffix=".html", mode="w", encoding="utf-8"
                )
                temp_file.write(html_content)
                temp_file.close()
                self.temp_file_path = temp_file.name
            except requests.RequestException as e:
                return f"Error fetching Tokopedia URL: {str(e)}"
            except Exception as e:
                return f"Error processing Tokopedia data: {str(e)}"

        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract product name
            name_elem = soup.find(
                "h1",
                class_="css-j63za0",
                attrs={"data-testid": "lblPDPDetailProductName"},
            )
            if not name_elem:
                return "No product name found in <div id='zeus-root'>."
            name = name_elem.text.strip() if name_elem else "N/A"

            # Placeholder for price
            price_elem = soup.find(
                "div",
                class_="price",
                attrs={"data-testid": "lblPDPDetailProductPrice"},
            )
            price = 0
            if name_elem:
                price = price_elem.text.strip()
                price = price.replace("Rp", "").replace(".", "").strip()

            image_urls = self._get_image_urls(soup)
            if image_urls:
                image_html = '<div style="display: flex; flex-wrap: wrap; gap: 10px;">'
                for url in image_urls:
                    image_html += f'<img src="{url}" style="width: 100px; height: 100px; object-fit: cover; border: 1px solid #ddd;"/>'
                image_html += "</div>"
                self.image_html = image_html
            else:
                self.image_html = "<p>No images found in <div class='css-17wadv5'>.</p>"

            preview = [f"1. Product Name: {name}", f"2. Price: {price}"]
            return "\n".join(preview)
        except Exception as e:
            return f"Error parsing temporary HTML: {str(e)}"

    def action_preview(self):
        """Preview Tokopedia data if selected, otherwise fall back to base behavior."""
        if self.source == "tokopedia.com":
            self.preview_data = self._scrape_tokopedia()
        else:
            return super().action_preview()
        return {
            "type": "ir.actions.act_window",
            "res_model": "import.product.wizard",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }

    def action_import(self):
        """Import previewed Tokopedia data into Odoo products, including images."""
        if self.source != "tokopedia.com":
            return super().action_import()
        if not self.preview_data or "Error" in self.preview_data:
            return {"type": "ir.actions.act_window_close"}

        lines = self.preview_data.split("\n")
        if not lines:
            return {"type": "ir.actions.act_window_close"}

        name = None
        price = 0.0
        for line in lines:
            line = line.strip()
            if line.startswith("1. "):
                name = line.split(":")[1].strip()
            elif line.startswith("2. "):
                price_str = line.split(":")[1].strip()
                price = (
                    float(price_str)
                    if price_str and price_str != "Price not available"
                    else 0.0
                )

        if name:
            try:
                soup = BeautifulSoup(self.image_html or "", "html.parser")
                image_urls = [
                    img["src"].replace("/100-square/", "/500-square/")
                    for img in soup.find_all("img")
                    if "src" in img.attrs
                ]

                image_binary = None
                if image_urls:
                    response = requests.get(image_urls[0], timeout=10)
                    response.raise_for_status()
                    image_binary = base64.b64encode(response.content).decode("utf-8")

                product_vals = {
                    "name": name,
                    "list_price": price,
                    "type": "consu",
                    "image_1920": image_binary,
                }
                product = self.env["product.template"].create(product_vals)

                if (
                    len(image_urls) > 1
                    and "product_template_image_ids"
                    in self.env["product.template"]._fields
                ):
                    additional_images = []
                    n = 0
                    for url in image_urls[1:]:

                        try:
                            response = requests.get(url, timeout=10)
                            response.raise_for_status()
                            image_binary = base64.b64encode(response.content).decode(
                                "utf-8"
                            )
                            n += 1
                            additional_images.append(
                                (
                                    0,
                                    0,
                                    {"image_1920": image_binary, "name": f"image_{n}"},
                                )
                            )
                        except Exception as e:
                            self.preview_data += (
                                f"\nError fetching image '{url}': {str(e)}"
                            )
                    if additional_images:
                        product.write({"product_template_image_ids": additional_images})

            except Exception as e:
                self.preview_data += f"\nError importing '{name}': {str(e)}"
        else:
            self.preview_data += "\nError: No valid product name found in preview."

        return {"type": "ir.actions.act_window_close"}
