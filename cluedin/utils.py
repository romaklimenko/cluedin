import base64
import json

# TODO: deprecate
def save(obj, filename, sort_keys=True):
    with open(filename, 'w') as file:
        json.dump(obj, file, ensure_ascii=False, indent=2, sort_keys=sort_keys)

# TODO: deprecate
def load(filename):
    with open(filename, 'r') as file:
        return json.load(file)


# TODO: deprecate
def parse_jwt_payload(jwt: str) -> dict:
    # Split the token into header, payload, and signature
    _, payload, _ = jwt.split('.')

    # Decode the payload from base64
    decoded_payload = base64.b64decode(payload + '=' * (4 - len(payload) % 4))

    # Convert the decoded payload to string
    return json.loads(decoded_payload.decode('utf-8'))
