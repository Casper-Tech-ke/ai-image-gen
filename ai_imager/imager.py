from . import logging, getExc, error_handler
from io import BytesIO
from PIL import Image, ImageStat
import requests
import colorsys
from math import ceil
from concurrent.futures import ThreadPoolExecutor, as_completed

CASPER_API_BASE = "https://apis.xcasper.space/api"


class openai_handler:
    def __init__(self, args: object):
        pass

    def _fetch_deepai_image(self, prompt: str) -> str | None:
        """Fetch one image URL from DeepAI endpoint."""
        try:
            resp = requests.get(
                f"{CASPER_API_BASE}/ai/deepai",
                params={"prompt": prompt},
                timeout=60,
            )
            data = resp.json()
            if data.get("success") and data.get("image_url"):
                return data["image_url"]
            logging.warning(f"DeepAI failed: {data.get('error', 'unknown error')}")
            return None
        except Exception as e:
            logging.error(f"DeepAI request error: {e}")
            return None

    def _fetch_magicstudio_image(self, prompt: str) -> str | None:
        """Fetch one image URL from Magic Studio endpoint."""
        try:
            resp = requests.get(
                f"{CASPER_API_BASE}/ai/magicstudio",
                params={"prompt": prompt},
                timeout=60,
            )
            data = resp.json()
            if data.get("success") and data.get("image_url"):
                return data["image_url"]
            logging.warning(f"MagicStudio failed: {data.get('error', 'unknown error')}")
            return None
        except Exception as e:
            logging.error(f"MagicStudio request error: {e}")
            return None

    @error_handler()
    def create_from_prompt(
        self, prompt: str, total_images: int = 2, image_size: str = "512x512"
    ):
        """Create images from a text prompt using xcasper.space DeepAI endpoint.

        Args:
            prompt (str): Description of the desired image
            total_images (int, optional): Number of images to generate. Defaults to 2.
            image_size (str, optional): Image size (ignored, xcasper returns fixed size).

        Returns:
            list|str: List of image URLs or error message
        """
        total_images = int(total_images)
        urls = []
        with ThreadPoolExecutor(max_workers=min(total_images, 4)) as executor:
            futures = [executor.submit(self._fetch_deepai_image, prompt) for _ in range(total_images)]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    urls.append(result)
        if not urls:
            return "Failed to generate images. Please try again."
        return urls

    @error_handler()
    def create_edit(
        self,
        original_image_path: str,
        masked_image_path: str,
        prompt: str,
        total_images: int = 1,
        image_size: str = "512x512",
        path_to_image=None,
    ) -> list:
        """Generate new images based on a text prompt (mask/edit via xcasper DeepAI).

        Note: xcasper.space doesn't support true inpainting, so this generates
        new images matching the prompt instead.
        """
        total_images = int(total_images)
        urls = []
        with ThreadPoolExecutor(max_workers=min(total_images, 4)) as executor:
            futures = [executor.submit(self._fetch_deepai_image, prompt) for _ in range(total_images)]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    urls.append(result)
        if not urls:
            return "Failed to generate images. Please try again."
        return urls

    @error_handler()
    def create_variation(
        self, path_to_image: str, total_images: int = 1, image_size: str = "512x512"
    ) -> list:
        """Generate image variations using xcasper.space Magic Studio endpoint.

        Note: xcasper.space doesn't support true image variations, so this generates
        new images using a generic creative prompt instead.
        """
        total_images = int(total_images)
        prompt = "a creative artistic variation, high quality, detailed"
        urls = []
        with ThreadPoolExecutor(max_workers=min(total_images, 4)) as executor:
            futures = [executor.submit(self._fetch_magicstudio_image, prompt) for _ in range(total_images)]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    urls.append(result)
        if not urls:
            with ThreadPoolExecutor(max_workers=min(total_images, 4)) as executor:
                futures = [executor.submit(self._fetch_deepai_image, prompt) for _ in range(total_images)]
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        urls.append(result)
        if not urls:
            return "Failed to generate images. Please try again."
        return urls

    @error_handler()
    def create_with_bing(
        self, prompt: str, total_images: int = 2, image_size: str = None
    ) -> list:
        """Generate images using xcasper.space Magic Studio endpoint."""
        total_images = int(total_images)
        urls = []
        with ThreadPoolExecutor(max_workers=min(total_images, 4)) as executor:
            futures = [executor.submit(self._fetch_magicstudio_image, prompt) for _ in range(total_images)]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    urls.append(result)
        if not urls:
            with ThreadPoolExecutor(max_workers=min(total_images, 4)) as executor:
                futures = [executor.submit(self._fetch_deepai_image, prompt) for _ in range(total_images)]
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        urls.append(result)
        if not urls:
            return "Failed to generate images. Please try again."
        return urls

    def _analyze_image_features(self, path_to_image: str) -> dict:
        """Use PIL to extract rich visual features from an uploaded image."""
        img = Image.open(path_to_image).convert("RGB")
        w, h = img.size

        # Dominant colours via quantize
        small = img.copy()
        small.thumbnail((150, 150))
        quantized = small.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
        palette_rgb = quantized.getpalette()[:24]  # 8 colours × 3 channels
        hex_colors = [
            "#{:02X}{:02X}{:02X}".format(palette_rgb[i], palette_rgb[i+1], palette_rgb[i+2])
            for i in range(0, 24, 3)
        ][:5]

        # Brightness, contrast, saturation
        stat = ImageStat.Stat(img)
        brightness = sum(stat.mean[:3]) / (3 * 255)   # 0‑1
        contrast   = sum(stat.stddev[:3]) / (3 * 128)  # 0‑1 (rough)

        # Avg saturation via HSV
        pixels = list(img.getdata())
        sample = pixels[::max(1, len(pixels) // 500)]
        sat_total = sum(colorsys.rgb_to_hsv(r/255, g/255, b/255)[1] for r, g, b in sample)
        avg_sat = sat_total / len(sample)

        # Colour temperature (red warmth vs blue cool)
        avg_r = stat.mean[0]; avg_b = stat.mean[2]
        temp = "warm"  if avg_r > avg_b + 15 else ("cool" if avg_b > avg_r + 15 else "neutral")

        # Aspect ratio
        ratio = w / h
        if ratio > 1.6:   orientation = "wide landscape (panoramic)"
        elif ratio > 1.1: orientation = "landscape"
        elif ratio < 0.7: orientation = "portrait"
        else:             orientation = "square"

        # Brightness label
        bri_label = "very dark" if brightness < 0.25 else "dark" if brightness < 0.45 else \
                    "medium" if brightness < 0.65 else "bright" if brightness < 0.82 else "very bright"

        # Contrast label
        con_label = "flat/low-contrast" if contrast < 0.25 else "moderate contrast" if contrast < 0.55 else "high contrast"

        # Saturation label
        sat_label = "muted/desaturated" if avg_sat < 0.2 else "natural" if avg_sat < 0.5 else "vivid/saturated"

        return {
            "hex_colors": hex_colors,
            "brightness": bri_label,
            "contrast": con_label,
            "saturation": sat_label,
            "color_temp": temp,
            "orientation": orientation,
            "resolution": f"{w}×{h}",
        }

    @error_handler()
    def image_to_prompt(self, path_to_image: str) -> str:
        """Analyse an uploaded image and return a creative AI generation prompt."""
        features = self._analyze_image_features(path_to_image)

        description = (
            f"Image characteristics extracted via computer vision analysis:\n"
            f"- Orientation / aspect: {features['orientation']}\n"
            f"- Brightness: {features['brightness']}\n"
            f"- Contrast: {features['contrast']}\n"
            f"- Colour saturation: {features['saturation']}\n"
            f"- Colour temperature: {features['color_temp']}\n"
            f"- Dominant colour palette (hex): {', '.join(features['hex_colors'])}\n"
        )

        meta_prompt = (
            f"{description}\n"
            "Using ONLY the visual data above, write a detailed, creative AI image-generation prompt "
            "that would recreate an image with these exact visual properties. "
            "Include specifics about lighting, mood, artistic style, colour palette, composition, and atmosphere. "
            "Output ONLY the prompt text, no preamble, no bullet points, no explanation."
        )

        try:
            resp = requests.get(
                f"{CASPER_API_BASE}/ai/gemini",
                params={"prompt": meta_prompt},
                timeout=30,
            )
            data = resp.json()
            if data.get("success") and data.get("reply"):
                return data["reply"].strip()
        except Exception as e:
            logging.error(f"Gemini prompt error: {e}")

        # Fallback: build a basic prompt from features alone
        return (
            f"A {features['orientation']} composition with a {features['color_temp']} colour palette, "
            f"dominated by {', '.join(features['hex_colors'][:3])}. "
            f"{features['brightness'].capitalize()} exposure, {features['contrast']}, {features['saturation']} colours. "
            "Cinematic quality, highly detailed, professional photography."
        )

    def _get_image_bytes(
        self, path_to_image: str, image_resolution: int = 512, no_mods: bool = False
    ) -> bytes:
        if no_mods:
            return open(path_to_image, "r+b")
        image = Image.open(path_to_image)
        image = image.resize((image_resolution, image_resolution))
        image = image.convert("RGBA")
        byte_stream = BytesIO()
        image.save(byte_stream, format="PNG")
        return byte_stream.getvalue()
