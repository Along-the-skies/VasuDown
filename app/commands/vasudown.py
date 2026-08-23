from app.utils.urls import is_valid_url,identify_platform
from app.services.metadata import get_metadata
from app.preview.builder import build_preview

def handle_vasudown(ack, respond, command):
    ack()

    url = command["text"].strip()

    if not is_valid_url(url):
        respond("Invalid URL.")
        return

    platform = identify_platform(url)

    if platform is None:
        respond("Unsupported platform.")
        return

    metadata = get_metadata(url)

    preview = build_preview(metadata)

    respond(
        text=preview["text"],
        blocks=preview["blocks"]
    )