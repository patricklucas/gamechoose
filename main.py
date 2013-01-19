#!/usr/bin/env python
from __future__ import absolute_import

import os

import staticconf

from gamechoose import app

CONFIG_PATH = "config.yaml"


def main():
    db_uri = staticconf.get_string('db_uri')
    secret_key = staticconf.get_string('secret_key')
    debug = staticconf.get_bool('debug', False)

    if os.path.exists(CONFIG_PATH):
        staticconf.YamlConfiguration(CONFIG_PATH, error_on_unknown=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri.value
    app.secret_key = secret_key.encode('latin1')

    app.run(debug=debug.value)


if __name__ == '__main__':
    main()
