from flask import Flask, render_template, request, redirect
from persistance import persistance_read, persistance_create, persistance_update, persistance_delete, app, create_tables



app = app
create_tables()

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
