import os
import bitjws
import json
from flask import Flask, request, current_app
from flask.ext.login import login_required
import logging
from logging.handlers import RotatingFileHandler

import cfg

COINS = [{'metal': 'AU', 'mint': 'perth'}, {'metal': 'AG', 'mint': 'perth'}]
app = Flask(__name__)
handler = RotatingFileHandler('tests.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)


@app.route('/coin', methods=['GET'])
def get_coins():
    return current_app.bitjws.create_response(COINS)


@app.route('/coin', methods=['POST'])
@login_required
def create_coin():
    coin = {}
    coin['metal'] = request.jws_payload.get('metal')
    coin['mint'] = request.jws_payload.get('mint')
    COINS.append(coin)
    return current_app.bitjws.create_response(coin)


@app.route('/echo', methods=['POST'])
@login_required
def echo():
    dd = request.jws_payload['data']
    return current_app.bitjws.create_response(dd)


@app.route('/echodetails', methods=['POST'])
@login_required
def echodetails():
    p = request.jws_payload
    h = request.jws_header
    response = {'headers': dict(request.headers), 'jws': 
                {'header': h, 'payload': p}}
    return current_app.bitjws.create_response(response)

@app.route('/user', methods=['POST'])
def prot():
    user = json.loads(request.get_data())
    oldu = current_app.bitjws.get_user_by_key(current_app, user['kid'])
    if oldu is not None:
        user = oldu
    else:
        user['salt'] = user['kid']  # just reusing this salt name... not a salt
        del user['kid']
        current_app.example_user_db[user['salt']] = user
    return json.dumps(user)

if __name__ == "__main__":
    from flask_bitjws import FlaskBitjws
    fbj = FlaskBitjws(app)
    app.run(host='0.0.0.0', port=8002, debug=True)

