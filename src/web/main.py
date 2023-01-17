#!/usr/bin/env python3

import flask

from flask import request
from flask import Flask

TEMPLATE_PATH = '../../data/web'

app = Flask(__name__, template_folder=TEMPLATE_PATH)

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        name = request.form["name"]
        return flask.render_template('hello.html', name=name)
    else:
        return flask.render_template('main.html')


if __name__ == '__main__':
    app.run()
