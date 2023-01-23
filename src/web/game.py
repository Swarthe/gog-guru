#!/usr/bin/env python3

import sqlite3 as sql

DB_PATH = 'data/game/games.db'

class Data:
    def __init__(self):
        with sql.connect(DB_PATH) as db:
            self.db = db
            # Enable reading rows into dictionaries
            self.db.row_factory = sql.Row

    # TODO
    def get(self, name: str) -> dict:
        # Use replacement pattern ('?') to avoid SQL injections.
        # There should only be one row, as every game name is unique.
        return self.db.execute('''
            SELECT * FROM Games
            WHERE name = ?
        ''', (name,)).fetchall()[0]
