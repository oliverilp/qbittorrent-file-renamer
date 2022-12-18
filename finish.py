import sys
import re
import os
from os import listdir
from os.path import isfile

BANNED_FILE_TYPES = (".txt", ".exe")
BANNED_WORDS = {
    "rarbg",
    "bluray",
    "blu-ray",
    "x264-",
    "x265-",
    "h264-",
    "h265-",
    "hevc",
    "bdrip",
    "webrip",
    "hdrip",
    "web-dl",
    "2160p",
    "1080p",
    "720p"
}


def get_filtered_name(file_name: str, count: int = 3):
    filtered = re.sub(
        r"(\[.*?\])|(\d{3,4}p)|(\((?!\d{4}).*?\))", "", file_name)
    if " " not in file_name and file_name.count(".") >= 3:
        # Replace dots with spaces
        filtered = re.sub(r"\.(?!\w{3}$)", " ", filtered)
    for word in BANNED_WORDS:
        filtered = re.sub(word, '', filtered, flags=re.IGNORECASE)

    # clean up whitespace
    filtered = re.sub(r"(\s+(?=\.\w+$))", "", filtered).strip()
    filtered = re.sub(r"(\s{2,})|(\.{2,})", " ", filtered)
    if count != 0:
        return get_filtered_name(filtered, count - 1) if len(filtered) > 4 else file_name
    return filtered


def clean_up_path(path: str, use_recursion=False):
    files = listdir(path)
    amount = 0
    for file_name in files:
        old_path = os.path.join(path, file_name)
        if isfile(old_path) and file_name.endswith(BANNED_FILE_TYPES):
            print(f"Removing file {file_name}.")
            os.remove(old_path)
            continue
        if use_recursion and not isfile(old_path):
            print(f"Recursion in directory {file_name}.")
            clean_up_path(old_path, True)

        new_name = get_filtered_name(file_name)
        if file_name != new_name:
            new_path = os.path.join(path, new_name)
            os.rename(old_path, new_path)
            amount += 1
    path = path[:-1] if path.endswith("/") else path
    base_name = os.path.basename(path)
    print(f"Renamed {amount} item{'' if amount == 1 else 's'} in path '{base_name}'.")


def main():
    if len(sys.argv) == 3:
        [file_name, save_path] = sys.argv[1:]
        file_path = os.path.join(save_path, file_name)

        if not isfile(file_path):
            clean_up_path(file_path, use_recursion=True)
        clean_up_path(save_path)


if __name__ == "__main__":
    main()
