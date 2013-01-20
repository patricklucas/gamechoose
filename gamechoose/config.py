from __future__ import absolute_import

import os

import staticconf

CONFIG_PATH = "config.yaml"

db_uri = staticconf.get_string('db_uri')
secret_key = staticconf.get_string('secret_key')
debug = staticconf.get_bool('debug', False)

user_blacklist = staticconf.get_list('user_blacklist', [])


def load():
    if os.path.exists(CONFIG_PATH):
        staticconf.YamlConfiguration(CONFIG_PATH, error_on_unknown=True)
