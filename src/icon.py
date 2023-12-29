from PIL import Image, ImageFont
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from pilmoji import Pilmoji
import os
import hashlib
import cairosvg
import base64

# Emoji support


def generate_emoji_image(app, tab) -> str:
    emoji = tab["icon"]
    base_image_size = 300  # Size of the base image
    font_size = 300  # Larger font size for a larger emoji

    with Image.new(
        "RGBA", (base_image_size, base_image_size), (255, 255, 255, 0)
    ) as image:
        font = ImageFont.truetype("./src/Roboto-Regular.ttf", font_size)

        with Pilmoji(image) as pilmoji:
            text_width, text_height = pilmoji.getsize(emoji, font=font)
            text_x = int((image.width - text_width) / 2)
            text_y = int((image.height - text_height) / 2)
            pilmoji.text((text_x, text_y), emoji, (0, 0, 0), font)
        app.logger.info(f"generated emoji image for {tab}")
        return image


# Favicon support


def find_favicons_in_html(html_content, base_url):
    soup = BeautifulSoup(html_content, "html.parser")
    # not including these since they seem to have backgrounds
    # "apple-touch-icon", "apple-touch-icon-precomposed"
    rel_types = ["shortcut icon", "icon"]
    found_favicons = set()

    # Find favicons specified in HTML
    for rel_type in rel_types:
        link_tag = soup.find("link", rel=rel_type)
        if link_tag and link_tag.get("href"):
            href = link_tag.get("href")
            # Complete the URL if it's relative
            if not href.startswith("http"):
                href = requests.compat.urljoin(base_url, href)
            found_favicons.add(href)

    # Add the default favicon.ico
    default_favicon = requests.compat.urljoin(base_url, "/favicon.ico")
    found_favicons.add(default_favicon)

    return list(found_favicons)


def create_image_from_url(favicon_url, base_url=None):
    try:
        # Determine if the image is SVG
        is_svg = favicon_url.endswith(".svg") or "data:image/svg+xml" in favicon_url

        if favicon_url.startswith("data:image"):
            # Decode Base64 encoded image
            image_data = base64.b64decode(favicon_url.split(",")[1])
            if is_svg:
                # Convert SVG data to PNG
                image_data = cairosvg.svg2png(bytestring=image_data)
            return Image.open(BytesIO(image_data))
        else:
            # Complete the URL if it's relative and base_url is provided
            if base_url and not favicon_url.startswith("http"):
                favicon_url = requests.compat.urljoin(base_url, favicon_url)

            # Download the favicon
            favicon_response = requests.get(favicon_url)

            if is_svg:
                # Convert SVG content to PNG
                image_data = cairosvg.svg2png(bytestring=favicon_response.content)
                return Image.open(BytesIO(image_data))
            else:
                return Image.open(BytesIO(favicon_response.content))
    except Exception as e:
        print(f"An error occurred while creating image: {e}")
        return None


def generate_favicon_image(app, tab):
    url = tab["url"]
    try:
        # Fetch the HTML content from the URL
        response = requests.get(url)
        html_content = response.content

        # Find all possible favicon locations
        favicon_urls = find_favicons_in_html(html_content, url)

        # Log the first 100 characters of each location
        for favicon_url in favicon_urls:
            print(f"Favicon URL: {favicon_url[:100]}")

        # Attempt to grab each favicon
        images = []
        for favicon_url in favicon_urls:
            image = create_image_from_url(favicon_url, base_url=url)
            if image:
                app.logger.info(f"downloaded {favicon_url} size: {image.size}")
                images.append(image)

        app.logger.info(f"found {len(images)} images for {tab}")
        if len(images) == 0:
            return None

        app.logger.info("sorting images by size")
        images.sort(key=lambda x: x.size, reverse=True)

        app.logger.info("images found:")
        for img in images:
            app.logger.info(img.size)

        return images[0]
    except Exception as e:
        app.logger.info(f"An error occurred: {e}")


# Generic support


def get_icon(app, tab) -> str:
    try:
        if tab["icon"] is not None and len(tab["icon"]) > 0:
            img = generate_emoji_image(app, tab)
        else:
            img = generate_favicon_image(app, tab)
        return crop_to_square_and_save(app, img)
    except Exception as e:
        app.logger.error(f"Failed to generate icon image for {tab}: {e}")
        return ""


def crop_to_square_and_save(app, image: Image.Image) -> str:
    # Get the bounding box
    bbox = image.getbbox()

    # Calculate the center and the size for the square crop
    center_x = (bbox[2] + bbox[0]) / 2
    center_y = (bbox[3] + bbox[1]) / 2
    crop_size = max(bbox[2] - bbox[0], bbox[3] - bbox[1])

    # Define the square bounding box with margin
    square_bbox = (
        center_x - crop_size / 2,
        center_y - crop_size / 2,
        center_x + crop_size / 2,
        center_y + crop_size / 2,
    )

    # Convert the result of map to a tuple
    square_bbox = tuple(map(int, square_bbox))

    # Crop the image with the adjusted bounding box
    cropped_img = image.crop(square_bbox)

    # Save the image
    image_bytes = BytesIO()
    cropped_img.save(image_bytes, format="PNG")
    image_bytes = image_bytes.getvalue()
    md5_hash = hashlib.md5(image_bytes).hexdigest()
    filename = f"{md5_hash}.png"
    save_path = os.path.join("src/static/img/generated/", filename)

    with open(save_path, "wb") as f:
        f.write(image_bytes)

    return filename
