#!/usr/bin/env python3

import sqlite3 as sql

DB_PATH = 'data/game/games.db'

class Data:
    def __init__(self):
        with sql.connect(DB_PATH) as db:
            self.db = db
            # Enable reading rows into dictionaries
            self.db.row_factory = sql.Row

    def get(self, name: str):
        '''
        Returns a `dict` with data pertaining to `name`.

        Returns `None` if `name` was not found.
        '''
        # Use replacement pattern ('?') to avoid SQL injections.
        results = self.db.execute('''
            SELECT * FROM Games
            WHERE name = ?
        ''', (name,)).fetchall()

        return first_of(results)

    def get_fuzzy(self, name_pat: str):
        '''
        Returns a `dict` with data pertaining to something like `name`.

        Returns `None` if `name` was not matched.
        '''
        # Use replacement pattern ('?') to avoid SQL injections.
        results = self.db.execute('''
            SELECT * FROM Games
            WHERE name LIKE ?
        ''', ('%' + name_pat + '%',)).fetchall()
        print(len(results))

        return first_of(results)

def first_of(l: list):
    '''
    Returns first element of `l` or `None`.
    '''
    return l[0] if len(l) > 0 else None
