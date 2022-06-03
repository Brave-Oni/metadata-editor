from flask import render_template
from .models import *
from . import app, db


@app.route("/", methods=["GET"])
def index():
    query = Devices.query.all()
    return render_template('index.html', devices=query)
