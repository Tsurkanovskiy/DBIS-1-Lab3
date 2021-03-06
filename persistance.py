from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
import os

DB_URL = os.environ.get("DATABASE_URL")
DB_URL = DB_URL.replace("postgres", "postgresql")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)

class players(db.Model):
    player_name = db.Column(db.Text, unique=True, nullable=False, primary_key=True)

class matches(db.Model):
    match_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    match_date = db.Column(db.DateTime, nullable=False)
    victory_status = db.Column(db.Boolean, nullable=False)
    expansion_name = db.Column(db.Text, nullable=False)
    player1_name = db.Column(db.Text, db.ForeignKey('players.player_name'), nullable=False)
    player2_name = db.Column(db.Text, db.ForeignKey('players.player_name'), nullable=False)
    player1_faction = db.Column(db.Text, nullable=False)
    player2_faction = db.Column(db.Text, nullable=False)
    player1 = db.relationship('players', lazy=True, foreign_keys=[player1_name])
    player2 = db.relationship('players', lazy=True, foreign_keys=[player2_name])

def create_tables():
    db.create_all()
    db.session.commit()


def persistance_read(url_name):
    if (url_name == "/"):
        return matches.query.all()
    else:
        return players.query.all()
    

def persistance_create(url_name, form_data):
    if (url_name == "/"):
        registered_players = players.query.all()

        date = form_data.get('match_date')
        date = datetime.strptime(date, '%Y-%m-%d')
        expansion = form_data.get('expansions')
        faction1 = form_data.get('faction1')
        faction2 = form_data.get('faction2')
        player_name1 = form_data.get('player_name1')
        if (player_name1 not in [x.player_name for x in registered_players]):
            new_pro_player = players(player_name = player_name1)
            db.session.add(new_pro_player)
            db.session.commit()
        player_name2 = form_data.get('player_name2')
        if (player_name2 not in [x.player_name for x in registered_players]):
            new_pro_player = players(player_name = player_name2)
            db.session.add(new_pro_player)
            db.session.commit()
        win_status = bool(form_data.get('Winner'))
        entry = matches(match_date = date, victory_status = win_status, expansion_name = expansion, player1_name = player_name1, player2_name = player_name2, player1_faction = faction1, player2_faction = faction2)
        db.session.add(entry)
        db.session.commit()
    else:
        player = form_data.get('player_name')
        entry = players(player_name = player)
        db.session.add(entry)
        db.session.commit()

def persistance_update(url_name, form_data):
    if (url_name == "/"):
        registered_players = players.query.all()

        date = form_data.get('match_date')
        date = datetime.strptime(date, '%Y-%m-%d')
        expansion = form_data.get('expansions')
        faction1 = form_data.get('faction1')
        faction2 = form_data.get('faction2')
        player_name1 = form_data.get('player_name1')
        player_name2 = form_data.get('player_name2')
        win_status = bool(form_data.get('Winner'))
        entry_id = int(form_data.get('edit_id'))
        if (player_name1 not in [x.player_name for x in registered_players]):
            new_pro_player = players(player_name = player_name1)
            db.session.add(new_pro_player)
            db.session.commit()
        if (player_name2 not in [x.player_name for x in registered_players]):
            new_pro_player = players(player_name = player_name2)
            db.session.add(new_pro_player)
            db.session.commit()

        match_to_edit = matches.query.filter_by(match_id = entry_id).first()
        match_to_edit.match_date = date
        match_to_edit.victory_status = win_status
        match_to_edit.expansion_name = expansion
        match_to_edit.player1_name = player_name1
        match_to_edit.player2_name = player_name2
        match_to_edit.player1_faction = faction1
        match_to_edit.player2_faction = faction2
        db.session.commit()
    else:
        old_name = str(form_data.get('edit_id'))
        player = form_data.get('player_name')
        player_to_edit = players.query.filter_by(player_name = old_name).first()
        player_to_edit.player_name = player
        db.session.commit()

def persistance_delete(url_name, form_data):
    if (url_name == "/"):
        entry_id = form_data.get("entry_id")
        match_to_delete = matches.query.filter_by(match_id = entry_id).first()
        db.session.delete(match_to_delete)
        db.session.commit()
    else:
        old_name = str(form_data.get('entry_id'))
        player_to_delete = players.query.filter_by(player_name = old_name).first()
        db.session.delete(player_to_delete)
        db.session.commit()
