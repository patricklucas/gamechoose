#!/usr/bin/env python

from gamechoose import db, Vote

session = db.session


def main():
    session.query(Vote).delete()
    session.commit()


if __name__ == '__main__':
    main()
