import socket
import ssl
from urllib.parse import urlparse
from requestlib.Requester import IRequester


class CustomRequester(IRequester):
    def __init__(self, port: int = 80, max_redirects: int = 5) -> None:
        self.port = port
        self.max_redirects = max_redirects

    def __compose_http_request(self, url: str) -> str:
        """Composes an HTTP GET request for the specified URL

        Args:
            url (str): The URL to request

        Returns:
            str: The composed HTTP request
        """
        method = "GET"
        # Parse the URL to get the host and path.
        # This could be done with regex, but using the built-in library is safer.
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path or "/"
        connection = "close"
        user_agent = "CustomRequester"
        accept = "text/html"
        request = f"{method} {path} HTTP/1.1\r\nHost: {host}\r\nConnection: {
            connection}\r\nUser-Agent: {user_agent}\r\nAccept: {accept}\r\n\r\n"
        return request

    def __parse_headers(self, response: str) -> dict:
        """Parses the headers from an HTTP response

        Args:
            response (str): The HTTP response

        Returns:
            dict: A dictionary containing the headers
        """
        headers = {}
        header_lines = response.split("\r\n\r\n", 1)[0].split("\r\n")
        for line in header_lines[1:]:
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()
        return headers

    def __get_status_code(self, response: str) -> int:
        """Gets the status code from an HTTP response

        Args:
            response (str): The HTTP response

        Returns:
            int: The status code
        """
        status_line = response.split("\r\n", 1)[0]
        status_code = int(status_line.split(" ")[1])
        return status_code

    def get(self, url: str, redirects: int = 0) -> str:
        if redirects > self.max_redirects:
            raise Exception("Too many redirects")

        parsed_url = urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path or "/"
        use_https = parsed_url.scheme == "https"
        port = 443 if use_https else 80

        # Open a socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if use_https:
                # Wrap the socket with SSL for HTTPS so we can send encrypted data
                context = ssl.create_default_context()
                s = context.wrap_socket(s, server_hostname=host)

            s.connect((host, port))
            request = self.__compose_http_request(url)
            s.sendall(request.encode())
            # Since TCP is a streaming protocol, we need to read in chunks
            # until we have the full response. Also TCP does not guarantee
            # a fixed number of bytes per read, so we need to keep reading
            # until we have all the data.
            response_chunks = []
            while True:
                chunk = s.recv(4096)  # Read in 4KB chunks
                if not chunk:
                    break
                response_chunks.append(chunk)
        # Join the chunks of bytes into a single string and decode it to text
        response = b"".join(response_chunks).decode()

        status_code = self.__get_status_code(response)
        if status_code in [301, 302]:
            headers = self.__parse_headers(response)
            if 'location' in headers:
                # Get the new URL from the Location header
                redirect_url = headers['location']
                if not redirect_url.startswith("http"):
                    redirect_url = f"{
                        parsed_url.scheme}://{host}{redirect_url}"
                print(f"Redirecting to: {redirect_url}")
                return self.get(redirect_url, redirects + 1)

        # Separate headers from the body
        headers, body = response.split("\r\n\r\n", 1)
        return body

    def get_html(self, url: str) -> str:
        return self.get(url)
