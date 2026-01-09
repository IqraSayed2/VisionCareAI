from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import os
import random
from werkzeug.utils import secure_filename
from .models import Detection
from . import db
from datetime import datetime, timedelta


main = Blueprint("main", __name__)

UPLOAD_FOLDER = "app/static/uploads"

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/about")
def about(): 
    return render_template("about.html")

@main.route("/learn")
def learn():
    return render_template("learn.html")

@main.route("/detect", methods=["GET", "POST"])
@login_required
def detect():
    if request.method == "POST":
        file = request.files.get("image")

        if not file:
            return redirect(url_for("main.detect"))

        filename = secure_filename(file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # ---------- DUMMY AI RESULT (FOR NOW) ----------
        diseases = {
            "Diabetic Retinopathy": random.randint(70, 90),
            "Glaucoma": random.randint(5, 20),
            "Cataract": random.randint(1, 10)
        }

        primary_disease = max(diseases, key=diseases.get)
        confidence = diseases[primary_disease]

        status = "Positive" if confidence >= 50 else "Negative"

        new_detection = Detection(
            image=f"uploads/{filename}",
            disease=primary_disease,
            confidence=confidence,
            status=status,
            user_id=current_user.id
        )

        db.session.add(new_detection)
        db.session.commit()

        return render_template(
            "analysis_result.html",
            image_path=f"uploads/{filename}",
            diseases=diseases,
            primary_disease=primary_disease,
            confidence=confidence
        )

    return render_template("detect.html")

@main.route("/history")
@login_required
def history():
    detections = Detection.query.filter_by(
        user_id=current_user.id
    ).order_by(Detection.created_at.desc()).all()

    total_scans = len(detections)
    normal_results = len([d for d in detections if d.status == "Negative"])
    last_7_days = len([
        d for d in detections
        if d.created_at >= datetime.utcnow() - timedelta(days=7)
    ])

    return render_template(
        "history.html",
        detections=detections,
        total_scans=total_scans,
        normal_results=normal_results,
        last_7_days=last_7_days
    )