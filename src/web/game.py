#!/usr/bin/env python3

import sqlite3 as sql

DB_PATH = 'data/game/games.db'

class Data:
    def __init__(self):
        # Prevent concurrency issues with Flask.
        with sql.connect(DB_PATH, check_same_thread=False) as db:
            self.db = db
            # Enable reading rows into dictionaries
            self.db.row_factory = sql.Row

    def get_by_id(self, i: int):
        '''
        Returns a `dict` with data pertaining to `i`.

        Returns `None` if `i` was not found.
        '''
        # Use replacement pattern ('?') to avoid SQL injections.
        results = self.db.execute('''
            SELECT * FROM Games
            WHERE id = ?
        ''', (i,)).fetchall()

        return first_of(results)

    def get_fuzzy(self, name_pat: str) -> list:
        '''
        Returns a list of data pertaining to matches to `name`.

        Returns `None` if `name` was not matched.
        '''
        results = self.db.execute('''
            SELECT * FROM Games
            WHERE name LIKE ?
        ''', ('%' + name_pat + '%',)).fetchall()

        return results

    def supports_lang(gameid: int, lang_name: str) -> bool:
        '''
        accepts 'Anglais', 'Français'
        '''
        results = self.db.execute('''
            FROM Games, GameLanguages, Languages
            WHERE Games.id = ?
              AND Games.id = GameLanguages.game_id
              AND GameLanguages.language_id = Languages.id
              AND Languages.name = ?;
        ''', (gameid, lang_name,)).fetchall()

        return len(results) > 0

    def supports_os(gameid: int, os_name: str) -> bool:
        '''
        accepts 'Windows', 'Linux', 'macOS'
        '''
        results = self.db.execute('''
            FROM Games, GameSystems, Systems
            WHERE Games.id = ?
              AND Games.id = GameSystems.game_id
              AND GameSystems.system_id = Systems.id
              AND Systems.name = ?;
        ''', (gameid, os_name,)).fetchall()

        return len(results) > 0

def first_of(l: list):
    '''
    Returns first element of `l` or `None`.
    '''
    return l[0] if len(l) > 0 else None
