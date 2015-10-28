# flask-bitjws [![PyPi version](https://img.shields.io/pypi/v/flask-bitjws.svg)](https://pypi.python.org/pypi/flask-bitjws/) [![Build Status](https://travis-ci.org/deginner/flask-bitjws.svg?branch=master)](https://travis-ci.org/deginner/flask-bitjws) [![Coverage](https://coveralls.io/repos/deginner/flask-bitjws/badge.svg?branch=master&service=github)](https://coveralls.io/github/deginner/flask-bitjws?branch=master) [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/deginner/bitjws?utm_source=share-link&utm_medium=link&utm_campaign=share-link)


Flask extension for [bitjws](https://github.com/g-p-g/bitjws) authentication.

## Installation

Flask-bitjws can be installed by running:

`pip install flask-bitjws`

## Install

By default it's expected that [secp256k1](https://github.com/bitcoin/secp256k1) is available, so install it before proceeding; make sure to run `./configure --enable-module-recovery`. If you're using some other library that provides the functionality necessary for this, check the __Using a custom library__ section of the bitjws README.

Flask-bitjws can be installed by running:

`pip install flask-bitjws`

##### Building secp256k1

In case you need to install the `secp256k1` C library, the following sequence of commands is recommended. If you already have `secp256k1`, make sure it was compiled from the expected git commit or it might fail to work due to API incompatibilities.

```
git clone git://github.com/bitcoin/secp256k1.git libsecp256k1
cd libsecp256k1
git checkout d7eb1ae96dfe9d497a26b3e7ff8b6f58e61e400a
./autogen.sh
./configure --enable-module-recovery
make
sudo make install
```


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

This get_bitjws_header_payload call is automatically done for incoming requests with content-type "application/jose", and the results are stored in the request.
  
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
