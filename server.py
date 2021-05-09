from flask import Flask, render_template, request, redirect
from persistance import persistance_read, persistance_create, persistance_update, persistance_delete, app, db


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

db.create_all()

@app.route("/")
def main():
	all_matches = persistance_read()
	return render_template("main.html", all_matches=all_matches)

@app.route("/create", methods=["POST"])
def addNewTitle():
    persistance_create(request.form) 
    return redirect("/")


@app.route("/update", methods=["POST"])
def update():
    persistance_update(request.form)
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    persistance_delete(request.form)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
