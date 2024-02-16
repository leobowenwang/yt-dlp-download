import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Check if yt-dlp is installed
try:
    subprocess.check_call(["yt-dlp", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except subprocess.CalledProcessError:
    print("yt-dlp is not installed. Please install yt-dlp before running this script.")
    exit(1)

# Function to find all "url.txt" files in subdirectories
def find_url_files(base_dir):
    url_files = []
    for root, dirs, files in os.walk(base_dir):
        if "url.txt" in files:
            url_files.append(os.path.join(root, "url.txt"))
    return url_files

# Function to download audio using yt-dlp
def download_audio_yt_dlp(subfolder, urls):
    for url in urls:
        url = url.strip()
        print(f"Downloading audio from '{url}' in subfolder '{subfolder}' using yt-dlp...")
        subprocess.run(["yt-dlp", "--download-archive", f"{subfolder}/.archive", "--output", f"{subfolder}/%(artist)s - %(title)s.%(ext)s", url])
    return f"Downloaded audio in subfolder '{subfolder}' using yt-dlp"

# Scan for "url.txt" files
url_files = find_url_files(".")

# Create a ThreadPoolExecutor to download audio in parallel
with ThreadPoolExecutor(max_workers=4) as executor:  # You can adjust the max_workers as needed
    futures = []
    for url_file in url_files:
        subfolder = os.path.dirname(url_file)
        with open(url_file, "r") as file:
            urls = file.readlines()
            # Use yt-dlp as the primary method and spotdl as a fallback
            future = executor.submit(download_audio_yt_dlp, subfolder, urls)
            futures.append(future)

    # Wait for all tasks to complete
    for future in futures:
        result = future.result()
        print(result)

print("All audio downloaded successfully!")
