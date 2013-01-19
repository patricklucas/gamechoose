gamechoose
==========

Choose a game to play with friends.

1. Create a virtualenv and install dependencies: `pip install -r requirements.txt`
2. Initialize the database with `./init_db.py'
3. Load games from `games.yaml` with `./load_games.py`
3. Run with `./main.py`

If you add games to `games.yaml` you can run `./sync_games` on-line. If you remove anything, you'll need to clear all votes with `./clear_votes.py` and then run `./load_games`.
