import base64
import json


def get_jwt_payload(jwt: str) -> dict:
    """Get the payload from a JWT.

    Args:
        jwt (str): JWT.

    Returns:
        dict: Payload.
    """
    # Split the token into header, payload, and signature
    _, payload, _ = jwt.split('.')

    # Decode the payload from base64
    decoded_payload = base64.b64decode(payload + '=' * (4 - len(payload) % 4))

    # Convert the decoded payload to string
    return json.loads(decoded_payload.decode('utf-8'))
