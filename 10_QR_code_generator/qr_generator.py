"""QR generation and export logic."""
from pathlib import Path
import qrcode
from qrcode.image.svg import SvgPathImage
from PIL import Image

class QRGenerator:
    def generate(self, payload, size=420, fill_color="#111111",
                 back_color="#FFFFFF", error_correction=None, logo_path=None):
        if not isinstance(payload, str) or not payload.strip():
            raise ValueError("QR content cannot be empty.")
        if size < 100 or size > 2000:
            raise ValueError("Size must be between 100 and 2000 pixels.")
        kwargs = {"box_size": 10, "border": 4}
        if error_correction is not None:
            kwargs["error_correction"] = error_correction
        qr = qrcode.QRCode(**kwargs)
        qr.add_data(payload)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")
        img = img.resize((size, size), Image.Resampling.NEAREST)
        if logo_path:
            self._add_logo(img, logo_path, size)
        return img

    def _add_logo(self, img, logo_path, size):
        path = Path(logo_path)
        if not path.exists():
            raise FileNotFoundError(f"Logo file not found: {path}")
        logo = Image.open(path).convert("RGBA")
        logo_size = max(24, int(size * 0.18))
        logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
        # White backing improves contrast around the logo.
        pad = max(6, int(size * 0.025))
        backing = Image.new("RGB", (logo.width + pad * 2, logo.height + pad * 2), "white")
        img.paste(backing, ((size - backing.width) // 2, (size - backing.height) // 2))
        img.paste(logo, ((size - logo.width) // 2, (size - logo.height) // 2), logo)

    def save(self, image, path, fmt="png", payload=None, fill_color="#111111",
             back_color="#FFFFFF", error_correction=None):
        path = Path(path)
        fmt = fmt.lower()
        if fmt == "svg":
            if not payload:
                raise ValueError("Payload is required for SVG export.")
            kwargs = {"image_factory": SvgPathImage, "box_size": 10, "border": 4}
            if error_correction is not None:
                kwargs["error_correction"] = error_correction
            qr = qrcode.QRCode(**kwargs)
            qr.add_data(payload)
            qr.make(fit=True)
            svg = qr.make_image(fill_color=fill_color, back_color=back_color)
            svg.save(str(path))
        elif fmt in ("png", "jpg", "jpeg"):
            output = image.convert("RGB")
            output.save(path, format="JPEG" if fmt in ("jpg", "jpeg") else "PNG", quality=95)
        else:
            raise ValueError("Supported formats: PNG, JPG, SVG.")
