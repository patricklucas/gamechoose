from __future__ import absolute_import, division, unicode_literals

from flask import Flask, redirect, render_template, request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy

from . import config

config.load()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri.value
app.secret_key = config.secret_key.encode('latin1')

db = SQLAlchemy(app)


class Game(db.Model):

    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True, nullable=False)
    price = db.Column(db.Integer) # cents
    purchase_url = db.Column(db.String)

    votes = db.relationship('Vote', backref='game')

    def __init__(self, name, **kwargs):
        self.name = name
        self.price = kwargs.pop('price', None)
        self.purchase_url = kwargs.pop('purchase_url', None)

    @property
    def price_str(self):
        if self.price is None:
            return None

        if self.price == 0:
            return "Free"

        return "$%01.2f" % (self.price / 100)

    @classmethod
    def all_games(cls):
        return db.session.query(cls)

    def __repr__(self):
        return "<Game(%s)>" % self.name


class Vote(db.Model):

    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True)
    who = db.Column(db.String, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

    def __init__(self, who, **kwargs):
        self.who = who

        self.game_id = kwargs.pop('game_id', None)
        self.game = kwargs.pop('game', None)

    @classmethod
    def votes_for(cls, who):
        return db.session.query(cls).filter(cls.who == who)

    def __repr__(self):
        return "<Vote(%s, %r)>" % (self.who, self.game or self.game_id)


@app.route("/")
def home():
    return redirect(url_for('results'))


@app.route("/results")
def results():
    vote_counts = [
        (vote.game, count)
        for vote, count in db.session.query(Vote, db.func.count().label('count')) \
            .group_by(Vote.game_id) \
            .order_by('count DESC') \
            .all()
    ]

    all_games = frozenset(Game.all_games().all())
    voted_games = frozenset(game for game, _ in vote_counts)
    unloved_game_counts = [(game, 0) for game in all_games - voted_games]

    def vote_count_sort((game, count)):
        return (-count, game.name)

    results = sorted(vote_counts + unloved_game_counts, key=vote_count_sort)

    voters = [
        who
        for (who,) in db.session.query(Vote.who) \
            .group_by(Vote.who) \
            .order_by(Vote.who) \
            .all()
    ]

    return render_template("results.html", results=results, voters=voters)


@app.route("/vote", methods=['GET', 'POST'])
def vote():
    if 'who' not in session:
        return redirect(url_for('whoami'))

    who = session['who']

    if request.method == 'GET':
        games = Game.all_games().order_by(Game.name).all()
        votes = frozenset(vote.game_id for vote in Vote.votes_for(who).all())
        return render_template("vote.html", who=who, games=games, votes=votes)

    selected_games = frozenset(request.form.getlist('vote'))

    db.session.query(Vote).filter(Vote.who == who).delete()

    for game_id in selected_games:
        game_id = int(game_id)
        db.session.add(Vote(who, game_id=game_id))

    db.session.commit()

    return redirect(url_for('results'), 303)


@app.route("/whoami", methods=['GET', 'POST'])
def whoami():
    if request.method == 'GET':
        return render_template("whoami.html")

    who = request.form['who']
    if not who:
        return redirect(url_for('whoami'), 303)

    session['who'] = who

    return redirect(url_for('vote'), 303)


@app.route("/logout")
def logout():
    del session['who']
    return redirect(url_for('home'))
