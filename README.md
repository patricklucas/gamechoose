gamechoose
==========

Choose a game to play with friends.

1. Create a virtualenv and install dependencies: `pip install -r requirements.txt`
2. Create `config.yaml` defining at minimum `db_uri` and `secret_key`. (See `gamechoose/config.py`)
3. Initialize the database with `./init_db.py`
4. Load games from `doc/games.yaml` with `./load_games.py`
5. Run with `./main.py`

If you only add games to `doc/games.yaml` you can run `./sync_games` on-line. If you remove anything, you'll need to clear all votes with `./clear_votes.py` and then run `./load_games`.
