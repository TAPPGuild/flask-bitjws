# flask-bitjws [![PyPi version](https://img.shields.io/pypi/v/flask-bitjws.svg)](https://pypi.python.org/pypi/flask-bitjws/) [![Build Status](https://travis-ci.org/deginner/flask-bitjws.svg?branch=master)](https://travis-ci.org/deginner/flask-bitjws) [![Coverage](https://coveralls.io/repos/deginner/flask-bitjws/badge.svg?branch=master&service=github)](https://coveralls.io/github/deginner/flask-bitjws?branch=master) [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/deginner/bitjws?utm_source=share-link&utm_medium=link&utm_campaign=share-link)


Flask extension for [bitjws](https://github.com/g-p-g/bitjws) authentication.

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

## Initialization

##### Initialize a flask_bitjws Application
The flask-bitjws package provides a Flask Application wrapper. To enable bitjws authentication, initialize FlaskBitjws with your flask app as the first argument.

``` Python
from flask import Flask
from flask_bitjws import FlaskBitjws

app = Flask(__name__)
FlaskBitjws(app)
```

##### Customizing LoginManager
Flask-bitjws uses [flask-login](https://github.com/maxcountryman/flask-login) to manage user login and authentication. By default,
the FlaskBitjws initialization will create a new LoginManager for you. If you need to customize, you can alternately provide your own. Just be aware that it's request_loader needs to be left as is.

``` Python
from flask import Flask
from flask_bitjws import FlaskBitjws
from flask.ext.login import LoginManager

# Your LoginManager
lm = LoginManager()

app = Flask(__name__)
FlaskBitjws(app, loginmanager=lm)
```

##### Initialize with private key

To provide a private key for your server to use in signing, include a privkey argument to Application.__init__().

``` Python
from flask import Flask
from flask_bitjws import FlaskBitjws

# Your bitjws private key in WIF
privkey = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"

app = Flask(__name__)
FlaskBitjws(app, privkey=privkey)
```

## Usage

##### Requests

For all routes that require login (i.e. wrapped in @login_required), the FlaskBitjws login manager will validate the bitjws headers and data, and match it up to a user.

If authentication is successful, the request will have two new attributes "jws_payload", and "jws_header".

If authentication fails, flask-login will return a 401 error.

```
from flask import Flask
from flask_bitjws import FlaskBitjws

# Your bitjws private key in WIF
privkey = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"

app = Flask(__name__)
FlaskBitjws(app, privkey=privkey)

@app.route('/user', methods=['POST'])
@login_required
def post_user():
    # request.jws_payload should exist and have the deserialized JWT claimset
    username = request.jws_payload.get('username')
    # request.jws_header should exist and have the sender's public key
    address = request.jws_header['kid']
    user = {'username': username, 'address': address}
    # return a bitjws signed and formatted response
    return current_app.create_bitjws_response(user)
```

##### Responses

When you're ready to respond, use the create_bitjws_response method to construct your response in bitjws format.

```
response_object = {'can be': 'a dict', 'or any': 'valid json'}
return current_app.create_bitjws_response(response_object)
```

## Your Database

Flask-bitjws comes with an example, in-memory data store for users and nonces. Using this example "database" is extremely insecure and unstable. It is recommended to provide bindings to your own persistent database for production use. This can be done by passing `FlaskBitjws.__init__` two functions: get_last_nonce, and get_user_by_key. These should do pretty much what their names say.

##### SQLAlchemy Example

```
def get_last_nonce(app, key, nonce):
    """
    This method is only an example! Replace it with a real nonce database.

    :param str key: the public key the nonce belongs to
    :param int nonce: the latest nonce
    """
    uk = ses.query(UserKey).filter(UserKey.key==key)\
            .filter(UserKey.last_nonce<nonce * 1000).first()
    if not uk:
        return None
    lastnonce = copy.copy(uk.last_nonce)
    # TODO Update DB record in same query as above, if possible
    uk.last_nonce = nonce * 1000
    try:
        ses.commit()
    except Exception as e:
        print e
        ses.rollback()
        ses.flush()
    return lastnonce


def get_user_by_key(app, key):
    """
    This method is only an example! Replace it with a real user database.

    :param str key: the public key the user belongs to
    """
    user = ses.query(SLM_User).join(UserKey).filter(UserKey.key==key).first()
    return user

FlaskBitjws(app, get_last_nonce=get_last_nonce,
            get_user_by_key=get_user_by_key)
```
