import os
import bitjws
from flask import Flask, jsonify, request, current_app, make_response, g

from flask_bitjws import Application, get_bitjws_header_payload

import cfg


app = Application(__name__)


COINS = [{'metal': 'AU', 'mint': 'perth'}, {'metal': 'AG', 'mint': 'perth'}]

@app.route('/noauth', methods=['GET'])
def get_coins():
    return current_app.create_bitjws_response(COINS)

@app.route('/auth', methods=['POST'])
def post_coin():
    if not hasattr(request, 'jws_header') or request.jws_header is None:
        return "Invalid Payload", 401
    coin = {}
    coin['metal'] = request.jws_payload.get('metal')
    coin['mint'] = request.jws_payload.get('mint')
    COINS.append(coin)
    return current_app.create_bitjws_response(coin)


@app.route('/echo', methods=['POST'])
def get_user():
    return {'headers': request.headers, 'data': request.get_data()}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002)
