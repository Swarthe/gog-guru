# GOG Guru

- Run `python run.py`
- Enter words pertaining to games you might like (e.g. space, rogue, zombie).
- Select constraints (language and OS)
- See games you might like

## Implementation

### Prerequisites

- List of GOG game [IDs][1]
- GOG API [documentation][2] (slightly outdated)

### Custom tools

- `mkdb`: creates a game database using the GOG API and game ID list

## Difficulties

- Outdated documentation for unofficial (unstable) API: actual requests don't
  match docs

[1]: https://gogapidocs.readthedocs.io/en/latest/gameslist.html
[2]: https://gogapidocs.readthedocs.io/en/latest/galaxy.html#api-gog-com

TODO: refresh db and schema image
TODO: make public on github ?

## License

This library is free software and subject to the MIT license. See `LICENSE.txt`
for more information.
