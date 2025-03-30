import base64
import json
from http import client


class PainterError(Exception):
    """Base exception for Painter-related errors."""

    def __init__(self, message):
        super().__init__(message)


class ExecuteScriptError(PainterError):
    """Exception raised when script execution fails."""

    def __init__(self, error_detail):
        super().__init__(f"An error occurred when executing script: {error_detail}")


class RemotePainter:
    """Interface to execute scripts remotely in Substance Painter."""

    def __init__(self, port=60041, host="localhost"):
        self._host = host
        self._port = port
        self._PAINTER_ROUTE = "/run.json"
        self._HEADERS = {"Content-type": "application/json", "Accept": "application/json"}

    def checkConnection(self):
        """Test connection to Substance Painter."""
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

    def execScript(self, script, type):
        """Execute a script in Substance Painter."""
        # Encode script to base64
        encoded_script = base64.b64encode(script.encode("utf-8")).decode("utf-8")
        # Format as JSON
        command = {"js" if type == "js" else "python": encoded_script}
        # Send as bytes
        command_bytes = json.dumps(command).encode("utf-8")
        return self._jsonPostRequest(self._PAINTER_ROUTE, command_bytes, type)

    def _jsonPostRequest(self, route, body, type):
        """Send a POST request to Substance Painter and process the JSON response."""
        connection = None
        try:
            connection = client.HTTPConnection(self._host, self._port, timeout=3600)
            connection.request("POST", route, body, self._HEADERS)
            response = connection.getresponse()
            data = response.read()
        finally:
            if connection:
                connection.close()

        print(f"Raw response: {data}")

        if not data:
            print("Empty response received")
            return {"status": "success"}

        decoded_data = None
        try:
            decoded_data = data.decode("utf-8")
            parsed_data = json.loads(decoded_data)
        except json.JSONDecodeError:
            print(f"Response is not JSON: {decoded_data}")
            return {"status": "success", "output": decoded_data}
        except UnicodeDecodeError as e:
            print(f"Error decoding response: {e}")
            return {"status": "error", "output": f"Unicode decoding error: {e}"}

        if parsed_data is None:
            print("Received null response, treating as success")
            return {"status": "success"}

        if not isinstance(parsed_data, dict):
            print(f"Unexpected response type: {type(parsed_data)}, treating as success")
            return {"status": "success", "output": str(parsed_data) if parsed_data else None}

        if "error" in parsed_data:
            if isinstance(body, bytes) and type == "js":
                try:
                    body_json = json.loads(body.decode("utf-8"))
                    if "js" in body_json:
                        print(base64.b64decode(body_json["js"]))
                except (json.JSONDecodeError, UnicodeDecodeError, base64.binascii.Error) as e:
                    print(f"Error processing error response body: {e}")
            raise ExecuteScriptError(parsed_data["error"])

        print("No error found in response")
        return parsed_data
