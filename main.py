#!/usr/bin/env python
from __future__ import absolute_import

from gamechoose import app, config


def main():
    app.run(debug=config.debug.value)


if __name__ == '__main__':
    main()
