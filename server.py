from flask import Flask, render_template, request, redirect
from persistance import persistance_read, persistance_create, persistance_update, persistance_delete, app, create_tables



app = app
create_tables()

@app.route("/")
def main():
	all_matches = persistance_read(str(request.url_rule))
	return render_template("main.html", all_matches=all_matches, page_url = str(request.url_rule))

@app.route("/players")
def players():
	all_players = persistance_read(str(request.url_rule))
	return render_template("players.html", players=all_players, page_url = str(request.url_rule))

@app.route("/create", methods=["POST"])
def addNewTitle():
    persistance_create(request.form.get('initialURL'), request.form) 
    return redirect("/")


@app.route("/update", methods=["POST"])
def update():
	persistance_update(request.form.get('initialURL'), request.form)
	return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    persistance_delete(request.form.get('initialURL'), request.form)
    return redirect("/")


if __name__ == "__main__":
    app.run()
