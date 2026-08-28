
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from app.utils.urls import is_valid_url, identify_platform
from app.services.metadata import get_metadata
from app.preview.builder import build_preview
from app.actions.download import handle_download


load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)


@app.command("/vasudown")
def vasudown_command(ack, client, command):
    ack()

    channel_id = command["channel_id"]
    url = command["text"].strip()

    if not is_valid_url(url):
        client.chat_postMessage(
            channel=channel_id,
            text="Invalid URL"
        )
        return

    platform = identify_platform(url)

    if platform is None:
        client.chat_postMessage(
            channel=channel_id,
            text="Unsupported Platform"
        )
        return

    metadata = get_metadata(url)
    print("METADATA:", metadata)
    preview = build_preview(metadata)

    client.chat_postMessage(
        channel=channel_id,
        text=preview["text"],
        blocks=preview["blocks"],
        response_type="in_channel",
    )


@app.action("open_media")
def open_media(ack):
    ack()


@app.action("download_media")
def download_media(ack, body, client):
    ack()

    url = body["actions"][0]["value"]

    result = handle_download(url)

    if result is None:
        client.chat_postMessage(
            channel=body["channel"]["id"],
            text="Download is not available yet."
        )
        return

    response = client.files_upload_v2(
        channel=body["channel"]["id"],
        file=result,
        title=os.path.basename(result),
    )

    if response.get("ok"):
        try:
            os.remove(result)
            print(f"Deleted '{result}' successfully after sending")
        except OSError as e:
            print(f"failed to delete cache Error : {e}")

@app.command("/vasudown-status")
def status(ack,client,command):
    ack()

    channel_id = command['channel_id']

    client.chat_postMessage(
        channel = channel_id,
        text="VasuDown is Online"
        )

@app.command("/vasudown-help")
def help(ack,client,command):
    channel_id = command["channel_id"]

    help_text = f"""Welcome to VasuDown
-------------------------------

VasuDown is a Slack bot that lets you download YouTube videos directly from Slack.

How to use
-------------------------------

1. Copy a YouTube video link.
2. Run `/vasudown <youtube_url>`
3. Wait for the video preview.
4. Click the Download button.
5. The video will be sent to the channel as a file.

Note:
Make sure you use a normal YouTube video link containing `watch?`.
Shorts and other YouTube link formats may not work.

-------------------------------

Use `/vasudown-status` to check if VasuDown is online."""
    ack()
    client.chat_postMessage(
        channel=channel_id,
        text=help_text
    )

    
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

