#!/usr/bin/env python
from __future__ import absolute_import

import yaml

from gamechoose import db, Game

GAMES_YAML = "games.yaml"

session = db.session


def main():
    with open(GAMES_YAML) as f:
        games = yaml.load(f)

    for game in games:
        if not session.query(Game).filter(Game.name == game['name']).count():
            new_game = Game(**game)
            print "Adding %r" % new_game
            session.add(new_game)

    session.commit()


if __name__ == '__main__':
    main()
