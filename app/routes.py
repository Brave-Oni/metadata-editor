import os

import plum.exceptions
from flask import render_template, request, flash, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
from .meta import meta
from .models import *
from . import app
from .form import EditForm


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            file = request.files["file"]
            filename = secure_filename(file.filename)
            filename = filename.split(".")
            filename = '.'.join([filename[0] + "_modify", filename[1]])
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)
            return redirect(url_for("info", filename=filename))
        except KeyError:
            flash("No file")
            redirect(request.url)
        except FileNotFoundError:
            redirect(request.url)

    return render_template("index.html")


@app.route("/info", methods=["GET", "POST"])
def info():
    filename = request.args['filename']
    location = "No info"
    try:
        image = meta.MetaImage(filename)
        location = image.get_location()
    except plum.exceptions.UnpackError:
        image = None

    form = EditForm()

    form.company.choices += [(company.id, company.name) for company in Companies.query.all()]
    form.models.choices = [(model.id, model.name) for model in Devices.query.filter_by(company_id=0).all()]

    if request.method == "POST":
        if form.validate_on_submit():
            make = Companies.query.filter_by(id=form.company.data).first()
            model = Devices.query.filter_by(id=form.models.data).first()
            date_time = form.datetime.data
            gps_latitude = form.gps_lat.data
            gps_longitude = form.gps_long.data
            gps_latitude_ref = form.gps_lat_ref.data
            gps_longitude_ref = form.gps_long_ref.data

            if make:
                image.set_metadata("make", make.name)
            if model:
                image.set_metadata("model", model.name)
            if date_time:
                image.set_metadata("datetime", date_time.strftime("%Y:%m:%d %H:%M:%S"))
            if gps_latitude:
                image.set_metadata("gps_latitude", tuple(map(float, gps_latitude.split())))
            if gps_longitude:
                image.set_metadata("gps_longitude", tuple(map(float, gps_longitude.split())))
            if gps_latitude_ref != "None":
                image.set_metadata("gps_latitude_ref", gps_latitude_ref)
            if gps_longitude_ref != "None":
                image.set_metadata("gps_longitude_ref", gps_longitude_ref)

            image.save(filename)
            return redirect(url_for("download", filename=filename))

    return render_template("info.html", image=image, form=form, location=location)


@app.route("/download", methods=["GET", "POST"])
def download():
    filename = request.args['filename']
    return send_file(os.path.join('upload', filename), as_attachment=True)


@app.route("/company/<company>")
def get_models(company):
    models = Devices.query.filter_by(company_id=company).all()

    models_list = []

    for model in models:
        model_object = {"id": model.id, "name": model.name}
        models_list.append(model_object)

    return jsonify({"models": models_list})
