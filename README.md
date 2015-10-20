# flask-bitjws
Flask extension for [bitjws](https://github.com/g-p-g/bitjws) authentication.

## Installation

At the moment, installing from source is the only supported method.

`python setup.py install`

## Usage

##### Initialize a flask_bitjws Application
The flask-bitjws package provides a Flask Application wrapper. To enable bitjws authentication, use the flask_bitjws.Application instead of flask.Flask to initialize your app.

``` Python
from flask_bitjws import Application

app = Application(__name__)
```

##### Initialize with private key

To provide a private key for your server to use in signing, include a privkey argument to Application.__init__().

``` Python
from flask_bitjws import Application

# Your bitjws private key in WIF
privkey = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"

app = Application(__name__, privkey=privkey)
```

##### Requests and Responses

To get the JWS header and payload from the raw request, use get_bitjws_header_payload. If the header returned is None, then the request failed signature validation.

This get_bitjws_header_payload call is automatically done for incoming requests with content-type "application/jws", and the results are stored in the request.
  
When you're ready to respond, use the create_bitjws_response method to construct your response in bitjws format.

```
from flask_bitjws import Application, get_bitjws_header_payload
app = Application(__name__)

# in memory users "database" for example
USERS = []

@app.route('/user', methods=['POST'])
def post_user():
    if not hasattr(request, 'jws_header') or request.jws_header is None:
        return "Invalid Payload", 401

    username = request.jws_payload.get('username')
    address = request.jws_header['kid']
    user = {'address': address, 'username': username}
    USERS.append(user)
    
    # return a bitjws signed and formatted response
    return current_app.create_bitjws_response(username=username,
            address=address, id=len(USERS))

app.run(host='0.0.0.0', port=8002)
```
