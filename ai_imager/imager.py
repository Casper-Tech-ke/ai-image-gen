from . import logging, getExc, error_handler
from io import BytesIO
from PIL import Image, ImageStat
import requests
import colorsys
import random
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed

POLLINATIONS_IMAGE_BASE = "https://image.pollinations.ai/prompt"
POLLINATIONS_TEXT_BASE  = "https://text.pollinations.ai"


class openai_handler:
    def __init__(self, args: object):
        pass

    def _pollinations_image_url(self, prompt: str, width: int = 512, height: int = 512) -> str:
        """Return a Pollinations.ai image URL for the given prompt.
        Each call uses a fresh random seed so parallel calls yield different images.
        """
        seed = random.randint(1, 999999)
        encoded = quote(prompt, safe="")
        return (
            f"{POLLINATIONS_IMAGE_BASE}/{encoded}"
            f"?width={width}&height={height}&seed={seed}&nologo=true"
        )

    def _fetch_pollinations_image(self, prompt: str, width: int = 512, height: int = 512) -> str | None:
        """Generate one image via Pollinations.ai and return a usable URL."""
        return self._pollinations_image_url(prompt, width, height)

    @error_handler()
    def create_from_prompt(
        self, prompt: str, total_images: int = 2, image_size: str = "512x512"
    ):
        """Create images from a text prompt using Pollinations.ai.

        Args:
            prompt (str): Description of the desired image
            total_images (int, optional): Number of images to generate. Defaults to 2.
            image_size (str, optional): WxH string, e.g. '512x512'.

        Returns:
            list|str: List of image URLs or error message
        """
        total_images = int(total_images)
        try:
            w, h = (int(x) for x in image_size.lower().split("x"))
        except Exception:
            w, h = 512, 512

        urls = []
        with ThreadPoolExecutor(max_workers=min(total_images, 4)) as executor:
            futures = [
                executor.submit(self._fetch_pollinations_image, prompt, w, h)
                for _ in range(total_images)
            ]
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
        """Generate new images based on a text prompt via Pollinations.ai.

        Note: Pollinations.ai does not support true inpainting, so this generates
        new images matching the prompt instead.
        """
        total_images = int(total_images)
        try:
            w, h = (int(x) for x in image_size.lower().split("x"))
        except Exception:
            w, h = 512, 512

        urls = []
        with ThreadPoolExecutor(max_workers=min(total_images, 4)) as executor:
            futures = [
                executor.submit(self._fetch_pollinations_image, prompt, w, h)
                for _ in range(total_images)
            ]
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
        """Generate image variations using Pollinations.ai.

        Extracts a rich visual description from the uploaded image using PIL,
        then uses that description as a prompt to generate inspired variations.
        """
        total_images = int(total_images)
        try:
            w, h = (int(x) for x in image_size.lower().split("x"))
        except Exception:
            w, h = 512, 512

        features = self._analyze_image_features(path_to_image)
        prompt = (
            f"A creative artistic variation with {features['color_temp']} tones, "
            f"dominant colors {', '.join(features['hex_colors'][:3])}, "
            f"{features['brightness']} exposure, {features['contrast']}, "
            f"{features['saturation']} palette, {features['orientation']} composition. "
            "High quality, detailed, artistic."
        )

        urls = []
        with ThreadPoolExecutor(max_workers=min(total_images, 4)) as executor:
            futures = [
                executor.submit(self._fetch_pollinations_image, prompt, w, h)
                for _ in range(total_images)
            ]
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
        """Generate images using Pollinations.ai (Magic Studio style)."""
        total_images = int(total_images)
        urls = []
        with ThreadPoolExecutor(max_workers=min(total_images, 4)) as executor:
            futures = [
                executor.submit(self._fetch_pollinations_image, prompt)
                for _ in range(total_images)
            ]
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

        small = img.copy()
        small.thumbnail((150, 150))
        quantized = small.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
        raw_palette = quantized.getpalette() or []
        usable = (len(raw_palette) // 3) * 3
        palette_rgb = raw_palette[:usable]
        hex_colors = [
            "#{:02X}{:02X}{:02X}".format(palette_rgb[i], palette_rgb[i+1], palette_rgb[i+2])
            for i in range(0, min(usable, 24), 3)
        ][:5] or ["#808080"]

        stat = ImageStat.Stat(img)
        brightness = sum(stat.mean[:3]) / (3 * 255)
        contrast   = sum(stat.stddev[:3]) / (3 * 128)

        pixels = list(img.getdata())
        sample = pixels[::max(1, len(pixels) // 500)]
        sat_total = sum(colorsys.rgb_to_hsv(r/255, g/255, b/255)[1] for r, g, b in sample)
        avg_sat = sat_total / len(sample)

        avg_r = stat.mean[0]; avg_b = stat.mean[2]
        temp = "warm" if avg_r > avg_b + 15 else ("cool" if avg_b > avg_r + 15 else "neutral")

        ratio = w / h
        if ratio > 1.6:   orientation = "wide landscape (panoramic)"
        elif ratio > 1.1: orientation = "landscape"
        elif ratio < 0.7: orientation = "portrait"
        else:             orientation = "square"

        bri_label = "very dark" if brightness < 0.25 else "dark" if brightness < 0.45 else \
                    "medium" if brightness < 0.65 else "bright" if brightness < 0.82 else "very bright"
        con_label = "flat/low-contrast" if contrast < 0.25 else "moderate contrast" if contrast < 0.55 else "high contrast"
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

        meta_prompt = (
            "Using ONLY the following visual data extracted from an image, write a detailed, "
            "creative AI image-generation prompt that would recreate an image with these exact "
            "visual properties. Include specifics about lighting, mood, artistic style, colour "
            "palette, composition, and atmosphere. Output ONLY the prompt text, no preamble.\n\n"
            f"Orientation: {features['orientation']}\n"
            f"Brightness: {features['brightness']}\n"
            f"Contrast: {features['contrast']}\n"
            f"Colour saturation: {features['saturation']}\n"
            f"Colour temperature: {features['color_temp']}\n"
            f"Dominant palette (hex): {', '.join(features['hex_colors'])}"
        )

        try:
            encoded = quote(meta_prompt, safe="")
            resp = requests.get(
                f"{POLLINATIONS_TEXT_BASE}/{encoded}",
                timeout=30,
            )
            if resp.status_code == 200 and resp.text.strip():
                return resp.text.strip()
        except Exception as e:
            logging.error(f"Pollinations text error: {e}")

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
