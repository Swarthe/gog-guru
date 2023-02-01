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

@app.route('/', methods=['POST', 'GET'])
def main():
    games = game.Data()

    if request.method == 'GET':
        return flask.render_template('main.html')
    else:
        game_search = request.form["game"]

        if len(game_search) == 0:
            return flask.render_template('main-err.html')
        else:
            game_data = games.get_fuzzy(game_search)
            dbg_dict(game_data)     # DEBUG

            if game_data is None:
                return flask.render_template(
                    "game-not-found.html",
                    game_search = game_search
                )
            else:
                return flask.render_template(
                    'game-result.html',
                    game_search = game_search,
                    game_data = game_data
                )

def dbg_dict(d):
    for v in d:
        print(f"k: {v}")

if __name__ == '__main__':
    app.run()

main()
