import os
import requests
from pathlib import Path
from typing import Optional
from typing import List


class ImageDownloader:
    
    @staticmethod
    def download_images_from_identifier(identifier: str, target_folder: Optional[str] = None):
        """
        Downloads all image files (e.g., .jpg, .png) associated with an Internet Archive identifier.

        Args:
            identifier (str): The identifier of the Internet Archive item.
            target_folder (str): Optional. The directory where images will be downloaded.
        """
        home_directory = Path.home()  # Gets the user's home directory, e.g., '/Users/username'
        if target_folder is None:
            target_dir = home_directory / "Music" / "Grateful Dead"
        else:
            target_dir = home_directory / "Music" / target_folder

        # Metadata URL to get all file details
        metadata_url = f"https://archive.org/metadata/{identifier}"

        try:
            response = requests.get(metadata_url)
            response.raise_for_status()
            data = response.json()

            # Get the files section from the metadata
            files = data.get('files', [])
            image_files = [file for file in files if file.get('format', '').lower() in ['jpeg', 'jpg', 'png', 'gif']]

            # Iterate over image files and download them
            for image in image_files:
                file_name = image.get('name')
                if not file_name:
                    continue

                # Construct the file download URL
                download_url = f"https://archive.org/download/{identifier}/{file_name}"

                # Determine the local path for saving
                local_path = os.path.join(target_dir, file_name)

                # Download and save the image file
                print(f"Downloading {file_name}...")
                image_response = requests.get(download_url, stream=True)
                image_response.raise_for_status()

                with open(local_path, 'wb') as f:
                    for chunk in image_response.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(f"Saved {file_name} to {local_path}")

        except requests.RequestException as e:
            print(f"Failed to fetch metadata or download images for identifier '{identifier}': {e}")


# Example usage:
if __name__ == "__main__":
    # Example identifier for a Grateful Dead show
    identifier = "gd1970-02-13.lateshow.mtx.131678.nicksmix.flac16"

    # Specify target directory for images
    target_directory = os.path.expanduser("~/Music/Grateful Dead/Images")

    # Download images associated with the identifier
    ImageDownloader.download_images_from_identifier(identifier, target_directory)
