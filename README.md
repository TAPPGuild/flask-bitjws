# flask-bitjws
Flask extension for bitjws authentication.

## Installation

At the moment, installing from source is the only supported method.

`python setup.py install`

## Usage

The flask-bitjws package provides a Flask Application wrapper. To enable bitjws authentication, use the flask_bitjws.Application instead of flask.Flask to initialize your app.

``` Python
from flask_bitjws import Application

app = Application()
```

To provide a private key for your server to use in signing, set 'BITJWS_PRIV_KEY' in the configuration passed in to Application.__init__().

``` Python
from flask_bitjws import Application

# Your bitjws private key in WIF
privkey = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"

app = Application(cfg)
```

To get the JWS header and payload from the raw request, use flask_bitjws.get_bitjws_header_payload. If the header returned is None, then the request failed signature validation.  
  
When you're ready to respond, use the create_bitjws_response method to construct your response in bitjws format.

```
from flask_bitjws import Application, get_bitjws_header_payload
app = Application(__name__)

# in memory users "database" for example
USERS = []

@app.route('/user', methods=['POST'])
def post_user():
    g.jws_header, g.payload = get_bitjws_header_payload(request)
    if g.jws_header is None:
        return "Invalid Payload", 401

    username = g.payload.get('username')
    address = g.jws_header['kid']
    user = User(address, username)
    USERS.append(user)
    response = current_app.create_bitjws_response(username=username,
            address=address, id=len(USERS))
    return response

app.run(host='0.0.0.0', port=8002)
```
