from __future__ import absolute_import

from gamechoose import db


def main():
    db.create_all()


if __name__ == '__main__':
    main()
