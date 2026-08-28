
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

    channel_id = client['channel_id']

    client.chat_postMessage(
        channel = channel_id,
        text="VasuDown is Online"
        )

@app.command("/vasudown-help")
def help(ack,client,command):

    help_text=f"Welcome to VasuDown\n-------------------------------\nVasudown is a slack bot to download youtube videos effortlessly\n-------------------------------\nHow to use\n --------\n get your youtube link -make sure it contain 'watch?' not 'shorts?' or something\n use command '/vasudown <youtube_url> \nwait for the preview\nOnce the preview loaded , click download\ndownload will send u the video as a file. you can download it by right clicking on the file\n-------------------------------\nUse '/vasudown-status' for the Bot status"

    ack()
    client.chat_postMessage(
        channel=channel_id,
        text=help_text
    )

    channel_id = client["channel_id"]
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

