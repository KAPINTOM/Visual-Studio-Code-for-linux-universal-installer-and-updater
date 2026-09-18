#!/usr/bin/env python3
"""
Downloads the latest VS Code stable build (tar.gz) for Linux x64,
removes any existing VSCode-linux-x64 folder, extracts the new
archive, and cleans up the tar.gz afterwards.
"""

import os
import shutil
import subprocess
import sys
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER_NAME = "VSCode-linux-x64"
FOLDER_PATH = os.path.join(SCRIPT_DIR, FOLDER_NAME)
ARCHIVE_NAME = "archive.tar.gz"
ARCHIVE_PATH = os.path.join(SCRIPT_DIR, ARCHIVE_NAME)
DOWNLOAD_URL = "https://code.visualstudio.com/sha/download?build=stable&os=linux-x64"


def remove_existing_folder():
    if os.path.exists(FOLDER_PATH):
        print(f"Removing existing folder: {FOLDER_PATH}")
        shutil.rmtree(FOLDER_PATH)
    else:
        print("No existing VSCode-linux-x64 folder found, skipping removal.")


def download_archive():
    print(f"Downloading VS Code from:\n  {DOWNLOAD_URL}")
    req = urllib.request.Request(
        DOWNLOAD_URL,
        headers={"User-Agent": "Mozilla/5.0"}  # some CDNs reject default UA
    )
    with urllib.request.urlopen(req) as response, open(ARCHIVE_PATH, "wb") as out_file:
        shutil.copyfileobj(response, out_file)
    print(f"Downloaded archive to: {ARCHIVE_PATH}")


def extract_archive():
    print(f"Extracting {ARCHIVE_NAME} ...")
    subprocess.run(
        ["tar", "-xvzf", ARCHIVE_NAME],
        cwd=SCRIPT_DIR,
        check=True
    )
    print("Extraction complete.")


def delete_archive():
    if os.path.exists(ARCHIVE_PATH):
        os.remove(ARCHIVE_PATH)
        print(f"Deleted archive: {ARCHIVE_PATH}")


def main():
    try:
        remove_existing_folder()
        download_archive()
        extract_archive()
        delete_archive()
        print("Done! VS Code has been updated.")
    except subprocess.CalledProcessError as e:
        print(f"Error running tar: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()