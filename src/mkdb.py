#!/usr/bin/env python3
#
# Creates a database of GOG games.
#
# Example (with created database):
#
# SELECT Languages.name
# FROM Games, GameLanguages, Languages
# WHERE Games.name = "140"
#   AND Games.id = GameLanguages.game_id
#   AND GameLanguages.language_id = Languages.id;
#
# To select languages supported by the game named "140".

import requests
import sqlite3 as sql

ID_LIST_PATH = 'data/game/id-list.txt'
DB_PATH = 'data/game/games.db'

# Maximum number of IDs in a single API request, according to GOG docs.
REQ_ID_COUNT = 50

API_URL = 'https://api.gog.com/products'

# Operating systems supported by games.
SYSTEMS = ["Windows", "Linux", "macOS"]
# Languages that we care about.
LANGUAGES = ["Anglais", "Français"]

def get_ids() -> list[str]:
    '''
    Parses the game ID list.

    Returns a list of ID groups suitable for API requests.
    '''
    with open(ID_LIST_PATH) as f:
        ids = [l for l in f.read().splitlines()]

    result = []

    for i in range(0, len(ids), REQ_ID_COUNT):
        # IDs in the API request should be comma-separated according to GOG
        # docs.
        req = ",".join(ids[i : i + REQ_ID_COUNT])
        result.append(req)

    return result

def get_data(ids: list[str]) -> list[dict]:
    '''
    Queries the GOG API for information pertaining to `ids`.

    `ids` must contain comma-separated lists of no more than `REQ_ID_COUNT` IDs.
    '''
    result = []

    for i in ids:
        # Get info for a groups of games.
        resps = requests.get(
            url=API_URL,
            params={ 'ids': i }
        ).json()

        # Flatten the response.
        for r in resps:
            result.append(r)

    return result

def create_db() -> sql.Connection:
    '''
    Create and initialise an SQLite database.
    '''
    with sql.connect(DB_PATH) as db:
        cur = db.cursor()

        # TODO: add fields (tags, price)
        # TODO: maybe voting and commenting functionality for users
        cur.executescript("""
            CREATE TABLE Games (
                id INTEGER PRIMARY KEY,
                name TEXT,
                release_year TEXT,
                is_released INTEGER,
                buy_url TEXT,
                help_url TEXT,
                forum_url TEXT,
                logo_url TEXT,
                bg_url TEXT
            );

            CREATE TABLE Systems (
                id INTEGER PRIMARY KEY,
                name TEXT
            );

            CREATE TABLE Languages (
                id INTEGER PRIMARY KEY,
                name TEXT
            );

            CREATE TABLE GameSystems (
                game_id INTEGER,
                system_id INTEGER,

                FOREIGN KEY(game_id) REFERENCES Games(id),
                FOREIGN KEY(system_id) REFERENCES Systems(id)
            );

            CREATE TABLE GameLanguages (
                game_id INTEGER,
                language_id INTEGER,

                FOREIGN KEY(game_id) REFERENCES Games(id),
                FOREIGN KEY(language_id) REFERENCES Languages(id)
            );
        """)

        for (i, s) in enumerate(SYSTEMS):
            # SQL IDs should start at 1.
            cur.execute(f"""
                INSERT INTO Systems (id, name) VALUES (
                    {i + 1}, "{s}"
                )
            """)

        for (i, l) in enumerate(LANGUAGES):
            # SQL IDs should start at 1.
            cur.execute(f"""
                INSERT INTO Languages (id, name) VALUES (
                    {i + 1}, "{l}"
                )
            """)

        return db

# TODO: find way to get game tags / categories
def populate_db(db: sql.Connection, data: list[str]):
    '''
    Populate an existing SQLite database.
    '''
    def populate_lang(cur: sql.Cursor, game_data: dict):
        langs = []

        if 'en' in d['languages'].keys():
            langs.append(LANGUAGES.index("Anglais"))
        if 'fr' in d['languages'].keys():
            langs.append(LANGUAGES.index("Français"))

        for c in langs:
            cur.execute(f'''
                INSERT INTO GameLanguages (game_id, language_id) VALUES (
                    {d['id']}, {c + 1}
                )
            ''')

    def populate_sys(cur: sql.Cursor, game_data: dict):
        sys = []

        if d['content_system_compatibility']['windows']:
            sys.append(SYSTEMS.index("Windows"))
        if d['content_system_compatibility']['linux']:
            sys.append(SYSTEMS.index("Linux"))
        if d['content_system_compatibility']['osx']:
            sys.append(SYSTEMS.index("macOS"))

        for c in sys:
            cur.execute(f'''
                INSERT INTO GameSystems (game_id, system_id) VALUES (
                    {d['id']}, {c + 1}
                )
            ''')

    cur = db.cursor()

    for d in data:
        # Some games don't have a release date.
        if d['release_date'] is not None:
            rel_date = d['release_date'][:4]
        elif d['in_development']['until'] is not None:
            rel_date = d['in_development']['until'][:4]
        else:
            rel_date = "unknown"

        cur.execute(f"""
            INSERT INTO Games VALUES (
                {d['id']},
                "{d['title']}",
                "{rel_date}",
                "{int(d['in_development']['active'])}",
                "{d['purchase_link']}",
                "{d['links']['support']}",
                "{d['links']['forum']}",
                "{'https://' + d['images']['logo2x'][2:]}",
                "{'https://' + d['images']['background'][2:]}"
            )
        """)

        populate_lang(cur, d)
        populate_sys(cur, d)


def main():
    ids = get_ids()

    print(":: Creating database...")
    with create_db() as db:
        print(":: Querying GOG API...")
        data = get_data(ids)

        print(":: Population database...")
        populate_db(db, data)

    print(":: Done!")

if __name__ == '__main__':
    main()
