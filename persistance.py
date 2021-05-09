from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://shadbceseekedm:2d223276263de89b4bf01fcae5428979582ed9a4699e578f22bea776d73d4aa6@ec2-54-216-48-43.eu-west-1.compute.amazonaws.com:5432/d22fs2rndonijb'
db = SQLAlchemy(app)

class players(db.Model):
	player_name = db.Column(db.Text, unique=True, nullable=False, primary_key=True)

class matches(db.Model):
	match_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
	match_date = db.Column(db.DateTime, nullable=False)
	victory_status = db.Column(db.Boolean, nullable=False)
	expansion_name = db.Column(db.Text, nullable=False)
	player1_name = db.Column(db.Text, nullable=False)
	player2_name = db.Column(db.Text, nullable=False)
	player1_faction = db.Column(db.Text, nullable=False)
	player2_faction = db.Column(db.Text, nullable=False)

def persistance_read():
	return matches.query.all()

def persistance_create(form_data):
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

def persistance_update(form_data):
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

def persistance_delete(form_data):
    entry_id = form_data.get("entry_id")
    match_to_delete = matches.query.filter_by(match_id = entry_id).first()
    db.session.delete(match_to_delete)
    db.session.commit()
