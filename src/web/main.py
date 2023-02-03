#!/usr/bin/env python3

import game

import flask

from flask import request
from flask import Flask

app = Flask(
    __name__,
    template_folder='data/templates',
    static_folder='data/static'
)

games = game.Data()

@app.route('/', methods=['POST', 'GET'])
def main():
    return flask.render_template('index.html')

@app.route('/eval_search', methods=['POST', 'GET'])
def eval_search():
    '''
    Evaluate and search the user input.
    '''
    search = request.form['search']
    data = games.get_fuzzy(search)

    if not search or not data:
        return flask.render_template(
            'invalid-search.html',
            search = search,
            data = data
        )
    else:
        if lang := request.form.get('lang'):
            data = filter(data,
                lambda d: games.supports_lang(d['id'], lang)
            )
        if os := request.form.get('os'):
            data = filter(data,
                lambda d: games.supports_os(d['id'], os)
            )

        return flask.render_template(
            'result.html',
            search = search,
            data = data
        )

@app.route('/game_info', methods=['POST', 'GET'])
def game_info():
    '''
    Load the information page for an individual game.
    '''
    return flask.render_template(
        'info.html',
        data = games.get_by_id(int(request.form['id']))
    )

if __name__ == '__main__':
    app.run()
