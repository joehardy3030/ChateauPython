import internetarchive as ia
from pathlib import Path
from typing import Optional
import os


def download_show(id, target_dir: Optional[str] = None):
    """
    Downloads an item from the Internet Archive using the identifier.

    Args:
        id (str): The identifier of the Internet Archive item to download.
        target_dir (str): The directory where the downloaded files should be saved.
                                          Defaults to '~/Music/Grateful Dead'.
    """
    # Set default target directory to 'Music/Grateful Dead' under user's home directory
    if target_dir is None:
        home_directory = Path.home()  # Gets the user's home directory, e.g., '/Users/username'
        target_dir = home_directory / "Music" / "Grateful Dead"

    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    print(f"Downloading item with identifier '{id}' to {target_dir}...")

    s = ia.get_session()
    s.mount_http_adapter()
    s_item = s.get_item(id)
    #s_item.metadata

    fnames = [f.name for f in s_item.get_files(id, glob_pattern='*mp3')]
    for f in fnames:
        s_item.download(f, destdir=target_dir)


if __name__ == "__main__":
    id = 'gd70-02-11.early-late.sbd.sacks.90.sbefail.shnf'
    download_show(id)
