import os
import yt_dlp

def progress_hook(download):
    if download["status"]=="downloading":
        percent = download.get("_percent_str","N/A").strip()
        speed = download.get("_speed_str","N/A").strip()
        eta = download.get("_eta_str","N/A").strip()

        print(
            f"Downloading : {percent} | Speed : {speed} | ETA : {eta}"
        
        )

    elif download["status"] == "finished":
        print("\nDownload Complete! Merging video and audio tracks...")

def download_youtube_video(video_url,output_folder="data"):
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts = {
    "format": "bv*+ba/b",
    "merge_output_format": "mp4",
    "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
    "progress_hooks": [progress_hook],
    "cookiefile": "cookies.txt",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        info = ydl.extract_info(video_url,download=False)
        filename=ydl.prepare_filename(info)

        return filename

#