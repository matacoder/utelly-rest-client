import os

import fire
import requests
from dotenv import load_dotenv
from requests import RequestException

load_dotenv()

TOKEN = os.getenv('TOKEN')
SERVER = os.getenv('SERVER')


class Movie:
    """Movie object."""

    def __init__(self, **kwargs):
        """Accept all dict fields as properties."""
        self.__dict__.update(kwargs)


class RestClient:
    """Connect to server with token."""

    def __init__(self, server, token):
        self.server = server
        self.token = token
        self.headers = self._get_headers()

    def _get_headers(self):
        """Build headers for authentication."""
        return {'X-AppKey': self.token}

    def _get_response(self, endpoint, **params):
        """Get response object from custom endpoint."""
        try:
            response = requests.get(
                self.server + endpoint,
                params=params,
                headers=self.headers
            )
            return response
        except RequestException as e:
            print(e)

    @staticmethod
    def _response_code_is_valid(response):
        return response.json().get('status_code') == 200

    def lookup_movies(self, term, endpoint='/lookup'):
        """Returns list of movies objects according search term."""
        response = self._get_response(endpoint, term=term)
        if response is not None:
            if self._response_code_is_valid(response):
                return self._convert_to_movies_2(response)

    @staticmethod
    def _convert_to_movies_2(response):
        """Keep movies as object to simplify properties lookup."""
        movies = []
        data = response.json()['results']
        for item in data:
            movies.append(Movie(**item))
        return movies


def search_tv_show_by_name(term='Star Trek'):
    """
    Perform search in movie database.

    ARG 1 = search term
    """
    client = RestClient(server=SERVER, token=TOKEN)
    movies = client.lookup_movies(term, endpoint='/lookup')
    if movies is not None:
        for title in movies:
            where_to_watch = ', '.join(
                list(map(lambda x: x['display_name'], title.locations))
            )
            print(f"{title.name}, available here: ({where_to_watch})")
    else:
        print("Something went wrong, can't get movies. "
              "Check API token and endpoint")


if __name__ == '__main__':
    fire.Fire(search_tv_show_by_name)
