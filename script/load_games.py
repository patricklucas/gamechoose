#!/usr/bin/env python
from __future__ import absolute_import

import sys

import yaml

from gamechoose import db, Game, Vote

GAMES_YAML = "doc/games.yaml"

session = db.session


def main():
    if session.query(Vote).count():
        sys.exit("Run clear_votes.py first.")

    session.query(Game).delete()

    with open(GAMES_YAML) as f:
        games = yaml.load(f)

    for game in games:
        new_game = Game(**game)
        print "Adding %r" % new_game
        session.add(new_game)

    session.commit()


if __name__ == '__main__':
    main()
