import bitjws
from flask import Flask, Response


def get_bitjws_header_payload(request):
    """
    :param flask.Request request: The raw request with bitjws message body
    :return: the JWS header and payload, in that order
    """
    header, payload = bitjws.validate_deserialize(
         request.get_data().decode('utf8'))
    if header is None:
        # Validation failed.
        return None
    return header, payload


class Application(Flask):
    """
    A wrapper for the main Flask application.
    """

    def __init__(self, name, privkey=None, **kwargs):
        """
        Initialize a Flask-bitjws Application.
        
        :param str name: the application's name
        :param str privkey: the bitjws private key to use for signing responses
        """
        super(Application, self).__init__(name, **kwargs)
        if privkey is not None and isinstance(privkey, str):
            self._privkey = bitjws.PrivateKey(bitjws.wif_to_privkey(privkey))
        elif privkey is not None and isinstance(privkey, bitjws.PrivateKey):
            self._privkey = privkey
        else:
            self._privkey = bitjws.PrivateKey()
        self.pubkey = bitjws.pubkey_to_addr(self._privkey.pubkey.serialize())
        print("Initializing server with address: {}".format(self.pubkey))


    def create_bitjws_response(self, **kwargs):
        """
        Create a signed bitjws response using the supplied keyword arguments.
        The response content-type will be 'application/jws'.
        """
        signedmess = bitjws.sign_serialize(self._privkey, **kwargs)
        return Response(signedmess, mimetype='application/jws')

