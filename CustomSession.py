'''
import json
from requests import Session, session
from requests.adapters import HTTPAdapter, Retry


class CustomSession:
    """
    A custom class for creating a session object with retries, timeouts, and headers.

    Attributes:
        session : session object for making HTTP requests
        headers: headers required for getting data from a website via API

    Methods:
        __init__(self, headers: dict = None) -> None:
            Initializes the CustomSession object with the given headers.

        get_session(self) -> Session:
            Returns the session object.

        hit_and_get_data(self, url: str, params: dict = None) -> dict:
            Hits the API and gets the data based on the endpoint and parameters passed.

    Args:
        headers : (optional) headers required for getting data from a website via API

    Returns:
        dict : JSON parsed result of the output response data from the API

    Raises:
        JSONDecodeError : If there is an error in decoding the JSON response
        Exception: If there is an error in connecting to the URL
    """

    def __init__(self, headers: dict = None) -> None:
        """
        Initializes a custom session with retries, timeouts, and optional headers.
        """
        self.session = session()

        # Set headers if provided
        self.headers = headers if headers else {}

        # Set retry strategy for failed requests
        retries = Retry(
            total=3,  # Total retry attempts
            backoff_factor=0.5,  # Wait time between retries (0.1 * 2^retry_attempts)
            status_forcelist=[500, 502, 503, 504, 400, 401, 402, 403]  # Status codes to retry on
        )

        # Mount the retry strategy to the session
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

        # Set timeout for each request (in seconds)
        self.session.timeout = 30

    def get_session(self) -> Session:
        """
        Returns the session object, allowing further customization if needed.
        """
        return self.session

    def hit_and_get_data(self, url: str, params: dict = None) -> dict:
        """
        Sends a GET request to the specified URL with optional parameters and returns the JSON response.

        Args:
            url: The API endpoint to hit.
            params: Optional query parameters for the GET request.

        Returns:
            dict: Parsed JSON response from the API or an empty dict in case of failure.
        """
        try:
            # Perform the GET request
            response = self.session.get(url, params=params, headers=self.headers)

            # Return the JSON response if available
            return response.json()
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from response at URL: {url}")
            return {}
        except Exception as err:
            print(f"Error in connecting to URL: {url} | Error: {err}")
            return {}
'''


import json
import time
from requests import Session, session
from requests.adapters import HTTPAdapter, Retry


class CustomSession:
    """
    A custom class for creating a session object with retries, timeouts, delays, and headers.

    Attributes:
        session : session object for making HTTP requests
        headers: headers required for getting data from a website via API

    Methods:
        __init__(self, headers: dict = None) -> None:
            Initializes the CustomSession object with the given headers.

        get_session(self) -> Session:
            Returns the session object.

        hit_and_get_data(self, url: str, params: dict = None) -> dict:
            Hits the API and gets the data based on the endpoint and parameters passed.

    Args:
        headers : (optional) headers required for getting data from a website via API

    Returns:
        dict : JSON parsed result of the output response data from the API

    Raises:
        JSONDecodeError : If there is an error in decoding the JSON response
        Exception: If there is an error in connecting to the URL
    """

    def __init__(self, headers: dict = None) -> None:
        """
        Initializes a custom session with retries, timeouts, optional headers, and delay.
        """
        self.session = session()

        # Set headers if provided
        self.headers = headers if headers else {}

        # Set retry strategy for failed requests
        retries = Retry(
            total=3,  # Total retry attempts
            backoff_factor=2,  # Increased wait time between retries (exponential backoff)
            status_forcelist=[500, 502, 503, 504, 400, 401, 402, 403]  # Status codes to retry on
        )

        # Mount the retry strategy to the session
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

        # Set timeout for each request (in seconds)
        self.session.timeout = 30

        # Add a delay (in seconds) between requests to slow down the process
        self.delay = 1  # Introducing a 5-second delay between requests

    def get_session(self) -> Session:
        """
        Returns the session object, allowing further customization if needed.
        """
        return self.session

    def hit_and_get_data(self, url: str, params: dict = None) -> dict:
        """
        Sends a GET request to the specified URL with optional parameters and returns the JSON response.
        Adds a delay between requests to slow down the process.

        Args:
            url: The API endpoint to hit.
            params: Optional query parameters for the GET request.

        Returns:
            dict: Parsed JSON response from the API or an empty dict in case of failure.
        """
        try:
            # Introduce a delay before making the request
            time.sleep(self.delay)
            
            # Perform the GET request
            response = self.session.get(url, params=params, headers=self.headers)

            # Return the JSON response if available
            return response.json()
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from response at URL: {url}")
            return {}
        except Exception as err:
            print(f"Error in connecting to URL: {url} | Error: {err}")
            return {}
