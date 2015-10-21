import os
import bitjws
from flask import request, current_app

from flask_bitjws import Application, get_bitjws_header_payload

import cfg

COINS = [{'metal': 'AU', 'mint': 'perth'}, {'metal': 'AG', 'mint': 'perth'}]

app = Application(__name__)


@app.route('/coin', methods=['GET'])
def get_coins():
    return current_app.create_bitjws_response(COINS)


@app.route('/coin', methods=['POST'])
def create_coin():
    if not hasattr(request, 'jws_header') or request.jws_header is None:
        return "Invalid Payload", 401
    coin = {}
    coin['metal'] = request.jws_payload.get('metal')
    coin['mint'] = request.jws_payload.get('mint')
    COINS.append(coin)
    return current_app.create_bitjws_response(coin)


@app.route('/echo', methods=['POST'])
def echo():
    h, p = get_bitjws_header_payload(request)
    return current_app.create_bitjws_response(p['echo'])


@app.route('/echodetails', methods=['POST'])
def echodetails():
    p = request.jws_payload
    h = request.jws_header
    response = {'headers': dict(request.headers), 'jws': 
                {'header': h, 'payload': p}}
    return current_app.create_bitjws_response(response)

