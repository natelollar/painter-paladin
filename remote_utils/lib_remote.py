"""Substance Painter Remote Executor
==================================================

A Python interface for remotely running scripts in Substance Painter via HTTP.
"""

import base64
import json
from http import client


class PainterError(Exception):
    """Base exception for Painter-related errors.

    Args:
        message: The error message describing the issue.

    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ExecuteScriptError(PainterError):
    """Exception raised when script execution fails.

    Args:
        error_detail: Details about the script execution failure.

    """

    def __init__(self, error_detail: str) -> None:
        super().__init__(f"An error occurred when executing script: {error_detail}")


class RemotePainter:
    """Interface to execute scripts remotely in Substance Painter.

    Args:
        port (int, optional): The port to connect to Substance Painter. Defaults to 60041.
        host (str, optional): The host address for Substance Painter. Defaults to "localhost".

    """

    def __init__(self, port: int = 60041, host: str = "localhost") -> None:
        self._host: str = host
        self._port: int = port
        self._PAINTER_ROUTE: str = "/run.json"
        self._HEADERS: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
        }

    def checkConnection(self) -> bool:
        """Tests the connection to Substance Painter.

        Returns:
            bool: True if the connection is successful.

        """
        connection = None
        try:
            connection = client.HTTPConnection(self._host, self._port, timeout=10)
            connection.connect()
            return True
        except Exception as e:
            raise PainterError(f"Failed to connect to {self._host}:{self._port}: {e}")
        finally:
            if connection:
                connection.close()

    def execScript(self, script: str, type: str) -> dict:
        """Executes a script in Substance Painter.

        Args:
            script: The script content to execute.
            type: The type of script ("js" for JavaScript, "python" for Python).

        Returns:
            dict: A dictionary with execution status and optional output.

        """
        # Encode script to base64 for transmission
        encoded_script: str = base64.b64encode(script.encode("utf-8")).decode("utf-8")
        # Format the command as JSON based on script type
        command: dict = {"js" if type == "js" else "python": encoded_script}
        # Convert command to bytes for HTTP request
        command_bytes: bytes = json.dumps(command).encode("utf-8")
        return self._jsonPostRequest(self._PAINTER_ROUTE, command_bytes, type)

    def _jsonPostRequest(self, route: str, body: bytes, type: str) -> dict:
        """Sends a POST request to Substance Painter and processes the JSON response.

        Args:
            route: The API route to send the request to.
            body: The encoded script data to send.
            type: The type of script ("js" for JavaScript, "python" for Python).

        Returns:
            dict: A dictionary containing the response status and optional output.

        """
        connection = None
        try:
            connection = client.HTTPConnection(self._host, self._port, timeout=3600)
            connection.request("POST", route, body, self._HEADERS)
            response = connection.getresponse()
            data = response.read()
        finally:
            if connection:
                connection.close()

        # Log the raw response for debugging
        print(f"Raw response: {data}")

        if not data:
            # Handle empty response as success
            print("Empty response received")
            return {"status": "success"}

        decoded_data = None
        try:
            decoded_data = data.decode("utf-8")
            parsed_data = json.loads(decoded_data)
        except json.JSONDecodeError:
            # Handle non-JSON response
            print(f"Response is not JSON: {decoded_data}")
            return {"status": "success", "output": decoded_data}
        except UnicodeDecodeError as e:
            # Handle decoding errors
            print(f"Error decoding response: {e}")
            return {"status": "error", "output": f"Unicode decoding error: {e}"}

        if parsed_data is None:
            # Treat null response as success
            print("Received null response, treating as success")
            return {"status": "success"}

        if not isinstance(parsed_data, dict):
            # Handle unexpected response types
            print(f"Unexpected response type: {type(parsed_data)}, treating as success")
            return {"status": "success", "output": str(parsed_data) if parsed_data else None}

        if "error" in parsed_data:
            # Debug JS script content on error
            if isinstance(body, bytes) and type == "js":
                try:
                    body_json = json.loads(body.decode("utf-8"))
                    if "js" in body_json:
                        print(base64.b64decode(body_json["js"]))
                except (json.JSONDecodeError, UnicodeDecodeError, base64.binascii.Error) as e:
                    print(f"Error processing error response body: {e}")
            raise ExecuteScriptError(parsed_data["error"])

        # Log success if no error found
        print("No error found in response")
        return parsed_data
