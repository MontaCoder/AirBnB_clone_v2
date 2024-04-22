#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """A route that displays a HTML page with the list of State objects"""
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """A route that removes the current SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
