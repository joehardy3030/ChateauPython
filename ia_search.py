import internetarchive
from typing import Optional, List, Dict


class SearchTermsModel:
    def __init__(self, search_term: Optional[str] = None, venue: Optional[str] = None,
                 start_year: Optional[str] = None, end_year: Optional[str] = None,
                 min_rating: Optional[str] = None, sbd_only: Optional[bool] = True):
        self.search_term = search_term
        self.venue = venue
        self.start_year = start_year
        self.end_year = end_year
        self.min_rating = min_rating
        self.sbd_only = sbd_only

    def to_query(self) -> str:
        """
        Converts the model to an Internet Archive query string.
        """
        query = 'collection:(GratefulDead AND stream_only)'

        if self.search_term:
            query += f' AND "{self.search_term}"'

        if self.venue:
            query += f' AND venue:"{self.venue}"'

        if self.start_year or self.end_year:
            start = self.start_year if self.start_year else "1965"
            end = self.end_year if self.end_year else "1995"
            query += f' AND date:[{start}-01-01 TO {end}-12-31]'

        if self.min_rating:
            query += f' AND avg_rating:[{self.min_rating} TO 5.0]'

        return query


def perform_archive_search(search_terms: SearchTermsModel) -> List[Dict[str, str]]:
    """
    Performs a search in the Internet Archive based on given search terms.

    Args:
        search_terms (SearchTermsModel): The parameters to use for the search.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing search result metadata.
    """
    # Convert the search terms to the proper query format
    query = search_terms.to_query()
    print(f"Performing search with query: {query}")

    # Request specific fields in the API call
    fields = ["identifier", "title", "date", "venue", "avg_rating"]

    # Search the Internet Archive using the internetarchive package
    results = internetarchive.search_items(query, fields=fields)

    # Collect search results to return
    results_list = []
    print(f"\nFound {results.num_found} results:\n")
    for item in results:
        # Extract fields with default values if they are missing
        result = {
            "identifier": item.get('identifier', 'No identifier available'),
            "title": item.get('title', 'No title available'),
            "date": item.get('date', 'No date available'),
            "venue": item.get('venue', 'No venue available'),
            "avg_rating": item.get('avg_rating', 'No rating available')
        }

        # Append to results list
        results_list.append(result)

        # Print details
        print(f"Identifier: {result['identifier']}")
        print(f"Title: {result['title']}")
        print(f"Date: {result['date']}")
        print(f"Venue: {result['venue']}")
        print(f"Rating: {result['avg_rating']}")
        print("-" * 40)

    return results_list


# Example Usage
if __name__ == "__main__":
    # Define your search terms
    search_terms = SearchTermsModel(
        search_term="Dark Star",
        venue="Fillmore East",
        start_year="1970",
        end_year="1971",
        min_rating="4",
        sbd_only=True
    )

    # Perform search with the provided search terms
    perform_archive_search(search_terms)
