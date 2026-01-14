from flask import Blueprint, render_template, request, redirect, url_for, make_response, abort, jsonify
from flask_login import login_required, current_user
import os
import random
from werkzeug.utils import secure_filename
from .models import Detection
from . import db
from datetime import datetime, timedelta
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

# Load the trained model
model = load_model('ml/visioncare_model.h5')



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

        # ---------- REAL AI PREDICTION ----------
        diseases, primary_disease, confidence = predict_eye_disease(filepath)

        status = "Negative" if primary_disease == "Normal" else "Positive"

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
            confidence=confidence,
            status=status,
            detection_id=new_detection.id
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

@main.route("/delete/<int:detection_id>", methods=["DELETE"])
@login_required
def delete_detection(detection_id):
    detection = Detection.query.get_or_404(detection_id)
    if detection.user_id != current_user.id:
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    # Delete the image file
    image_path = os.path.join("app/static", detection.image)
    if os.path.exists(image_path):
        os.remove(image_path)

    db.session.delete(detection)
    db.session.commit()

    return jsonify({"success": True})


@main.route("/export/<int:detection_id>")
@login_required
def export_report(detection_id):
    detection = Detection.query.get_or_404(detection_id)
    if detection.user_id != current_user.id:
        abort(403)

    # Create PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "VisionCare AI Report")

    # Details
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 130, f"Patient: {current_user.username}")
    c.drawString(100, height - 150, f"Date: {detection.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, height - 170, f"Disease: {detection.disease}")
    c.drawString(100, height - 190, f"Confidence: {detection.confidence}%")
    c.drawString(100, height - 210, f"Status: {detection.status}")

    # Add image
    image_path = os.path.join("app/static", detection.image)
    if os.path.exists(image_path):
        c.drawImage(image_path, 100, height - 350, width=200, height=120, preserveAspectRatio=True)

    # Note
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(100, height - 380, "Note: This is a preliminary AI analysis. Consult a doctor for confirmation.")

    c.save()

    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename=report_{detection_id}.pdf"
    response.headers["Content-Type"] = "application/pdf"
    return response


def predict_eye_disease(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Invalid image file")

    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img)[0]

    results = {
        "Cataract": int(preds[0] * 100),
        "Diabetic Retinopathy": int(preds[1] * 100),
        "Glaucoma": int(preds[2] * 100),
        "Normal": int(preds[3] * 100),
    }

    primary_disease = max(results, key=results.get)
    confidence = results[primary_disease]

    return results, primary_disease, confidence
