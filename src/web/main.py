#!/usr/bin/env python3

import game

import flask

from flask import request
from flask import Flask

TEMPLATE_PATH = 'data/web'

app = Flask(__name__, template_folder=TEMPLATE_PATH)

@app.route('/', methods=['POST', 'GET'])
def main():
    games = game.Data()

    if request.method == 'POST':
        req = user_request()

        if req is None:
            return flask.render_template('req-again.html')
        else:
            name = req['game']

            return flask.render_template(
                'res.html',
                logo_url = games.get(name)['logo_url'],
                **req
            )
    else:
        return flask.render_template('req.html')

@app.route('/')
def user_request() -> dict:
    req = request.form

    for v in req.values():
        if len(v) == 0:
            return None

    return req


if __name__ == '__main__':
    app.run()

main()
