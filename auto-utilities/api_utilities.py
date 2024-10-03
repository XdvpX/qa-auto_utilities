import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth1


class ApiClient:

    AUTH_TYPES = {'oauth1', 'basic', None}

    @classmethod
    def get_resource(cls, url: str, auth_type: str = None, headers: dict = None, credentials: dict = None,
                       follow_redirects: bool = True):
        """
        Fetch a resource using the GET method.

        Args:
            url: Endpoint URL to send the request to.
            auth_type: Authentication method to be used (default: None).
            headers: Optional dictionary of HTTP headers.
            credentials: Optional dictionary of credentials for authentication.
            follow_redirects: Allow redirection of the request (default: True).

        Returns:
            Response object from the GET request.
        """
        auth = cls._set_auth(auth_type=auth_type, credentials=credentials)
        return requests.get(url, auth=auth, headers=headers, allow_redirects=follow_redirects)

    @classmethod
    def delete_resource(cls, url: str, auth_type: str = None, headers: dict = None, credentials: dict = None,
                        follow_redirects: bool = True):
        """
        Remove a resource using the DELETE method.

        Args:
            url: Endpoint URL to send the request to.
            auth_type: Authentication method to be used (default: None).
            headers: Optional dictionary of HTTP headers.
            credentials: Optional dictionary of credentials for authentication.
            follow_redirects: Allow redirection of the request (default: True).

        Returns:
            Response object from the DELETE request.
        """
        auth = cls._set_auth(auth_type=auth_type, credentials=credentials)
        return requests.delete(url, auth=auth, headers=headers, allow_redirects=follow_redirects)

    @classmethod
    def patch_resource(cls, url: str, data: any = None, auth_type: str = None, headers: dict = None, files=None,
                        credentials: dict = None, follow_redirects: bool = True):
        """
        Update an existing resource using the PATCH method.

        Args:
            url: Endpoint URL to send the request to.
            data: Payload data to be sent with the request.
            auth_type: Authentication method to be used (default: None).
            headers: Optional dictionary of HTTP headers.
            files: Optional file upload.
            credentials: Optional dictionary of credentials for authentication.
            follow_redirects: Allow redirection of the request (default: True).

        Returns:
            Response object from the PATCH request.
        """
        auth = cls._set_auth(auth_type=auth_type, credentials=credentials)
        return requests.patch(url, data=data, auth=auth, headers=headers, files=files, allow_redirects=follow_redirects)

    @classmethod
    def post_resource(cls, url: str, payload: any, auth_type: str = None, headers: dict = None, files=None,
                        credentials: dict = None, follow_redirects: bool = True):
        """
        Create a new resource using the POST method.

        Args:
            url: Endpoint URL to send the request to.
            payload: Payload data to be sent with the request.
            auth_type: Authentication method to be used (default: None).
            headers: Optional dictionary of HTTP headers.
            files: Optional file upload.
            credentials: Optional dictionary of credentials for authentication.
            follow_redirects: Allow redirection of the request (default: True).

        Returns:
            Response object from the POST request.
        """
        auth = cls._set_auth(auth_type=auth_type, credentials=credentials)
        return requests.post(url, data=payload, auth=auth, headers=headers, files=files, allow_redirects=follow_redirects)

    @classmethod
    def put_resource(cls, url: str, payload=None, auth_type: str = None, headers: dict = None, files=None,
                         credentials: dict = None, follow_redirects: bool = True):
        """
        Replace an existing resource using the PUT method.

        Args:
            url: Endpoint URL to send the request to.
            payload: Data payload to be sent with the request (optional).
            auth_type: Authentication method to be used (default: None).
            headers: Optional dictionary of HTTP headers.
            files: Optional file upload.
            credentials: Optional dictionary of credentials for authentication.
            follow_redirects: Allow redirection of the request (default: True).

        Returns:
            Response object from the PUT request.
        """
        auth = cls._set_auth(auth_type=auth_type, credentials=credentials)
        return requests.put(url, data=payload, auth=auth, headers=headers, files=files, allow_redirects=follow_redirects)

    @classmethod
    def _set_auth(cls, auth_type: str, credentials: dict = None):
        """
        Helper method to configure authentication based on the provided credentials.

        Args:
            auth_type: Type of authentication ('oauth1' or 'basic').
            credentials: Dictionary containing the authentication credentials.

        Returns:
            Authentication object or None if no authentication is used.

        Raises:
            ValueError: If the authentication type is invalid or unsupported.
        """
        if auth_type not in cls.AUTH_TYPES:
            raise ValueError(f"Unsupported authentication method: {auth_type}. Valid options: {cls.AUTH_TYPES}")

        if auth_type == 'oauth1':
            return OAuth1(credentials['application_key'], credentials['application_secret'])
        elif auth_type == 'basic':
            return HTTPBasicAuth(credentials['username'], credentials['password'])
        return None
