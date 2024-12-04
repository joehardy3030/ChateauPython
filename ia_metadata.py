import requests
from typing import Optional, List


class ShowMetadata:
    def __init__(self, identifier: Optional[str] = None, title: Optional[str] = None,
                 creator: Optional[str] = None, mediatype: Optional[str] = None,
                 collection: Optional[List[str]] = None, item_type: Optional[str] = None,
                 description: Optional[str] = None, date: Optional[str] = None,
                 year: Optional[str] = None, venue: Optional[str] = None,
                 transferer: Optional[str] = None, source: Optional[str] = None,
                 coverage: Optional[str] = None, notes: Optional[str] = None):
        self.identifier = identifier
        self.title = title
        self.creator = creator
        self.mediatype = mediatype
        self.collection = collection
        self.item_type = item_type
        self.description = description
        self.date = date
        self.year = year
        self.venue = venue
        self.transferer = transferer
        self.source = source
        self.coverage = coverage
        self.notes = notes

    @classmethod
    def from_identifier(cls, identifier: str):
        """
        Fetch metadata for a given identifier and return an instance of ShowMetadata.

        Args:
            identifier (str): The identifier of the Internet Archive item.

        Returns:
            ShowMetadata: An instance of ShowMetadata with the fetched metadata.
        """
        base_url = "https://archive.org/metadata/"
        url = f"{base_url}{identifier}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()

            metadata = data.get('metadata', {})
            print(metadata)
            # Extract fields from the metadata
            return cls(
                identifier=identifier,
                title=metadata.get('title'),
                creator=metadata.get('creator'),
                mediatype=metadata.get('mediatype'),
                collection=metadata.get('collection'),
                item_type=metadata.get('type'),
                description=metadata.get('description'),
                date=metadata.get('date'),
                year=metadata.get('year'),
                venue=metadata.get('venue'),
                transferer=metadata.get('transferer'),
                source=metadata.get('source'),
                coverage=metadata.get('coverage'),
                notes=metadata.get('notes')
            )
        except requests.RequestException as e:
            print(f"Failed to fetch metadata for identifier '{identifier}': {e}")
            return None

    def __str__(self):
        """
        String representation of the ShowMetadata object for easy printing.
        """
        return (
            f"Identifier: {self.identifier}\n"
            f"Title: {self.title}\n"
            f"Creator: {self.creator}\n"
            f"Media Type: {self.mediatype}\n"
            f"Collection: {self.collection}\n"
            f"Type: {self.item_type}\n"
            f"Description: {self.description}\n"
            f"Date: {self.date}\n"
            f"Year: {self.year}\n"
            f"Venue: {self.venue}\n"
            f"Transferer: {self.transferer}\n"
            f"Source: {self.source}\n"
            f"Coverage: {self.coverage}\n"
            f"Notes: {self.notes}\n"
        )


# Example Usage:
if __name__ == "__main__":
    # Example identifier for a Grateful Dead show
    identifier = "gd1980-10-29.aud-sbd.tetzeli.join-1953-32538.35029.reflac.flac16"

    # Fetch metadata and print it
    show_metadata = ShowMetadata.from_identifier(identifier)
    if show_metadata:
        print(show_metadata)
