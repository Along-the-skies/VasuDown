def build_preview(metadata):
    if metadata is None:
        return {
            "text":"Unsupported media URL."
        }

    platform = metadata["platform"]
    url = metadata["url"]
    title = metadata.get("title") or "Untitled media"
    thumbnail = metadata.get("thumbnail")

    blocks = [
        {
            "type":"section",
            "text": {
                "type":"mrkdwn",
                "text": f"*{title}*\nPlatform:`{platform}`"
            }
        }
    ]

    if thumbnail:
        blocks.append({
            "type":"image",
            "image_url": thumbnail,
            "alt_text": title
        })

    blocks.append({
        "type":"actions",
        "elements": [
            {
                "type":"button",
                "text":{
                    "type":"plain_text",
                    "text":"Open"
                },
                "url":url,
                "action_id":"open_media"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Download"
                },
                "action_id": "download_media",
                "value": url
            }
        ]
    })

    return {
        "text":f"{title} ({platform})",
        "blocks":blocks
    }