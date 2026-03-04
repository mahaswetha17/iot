from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hospital-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'

db = SQLAlchemy(app)

# ---------------- MODELS ---------------- #

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    specialization = db.Column(db.String(100))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    condition = db.Column(db.String(200))
    medication = db.Column(db.String(200))
    next_appointment = db.Column(db.String(100))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))

# ---------------- ROUTES ---------------- #

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        if role == "doctor":
            return redirect(url_for("doctor_dashboard"))
        else:
            return redirect(url_for("patient_dashboard", patient_id=1))
    return render_template("login.html")

@app.route("/doctor")
def doctor_dashboard():
    doctors = Doctor.query.all()
    patients = Patient.query.all()
    return render_template("doctor_dashboard.html",
                           doctors=doctors,
                           patients=patients)

@app.route("/patient/<int:patient_id>")
def patient_dashboard(patient_id):
    patient = Patient.query.get(patient_id)
    
    # Generate sample health data for chart
    health_data = [random.randint(70, 120) for _ in range(7)]
    
    return render_template("patient_dashboard.html",
                           patient=patient,
                           health_data=health_data)

# ---------------- INITIALIZE DB ---------------- #

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        if not Doctor.query.first():
            d1 = Doctor(name="Dr. Meera Nair", specialization="Cardiologist")
            d2 = Doctor(name="Dr. Arjun Pillai", specialization="Endocrinologist")
            db.session.add_all([d1, d2])
            db.session.commit()

        if not Patient.query.first():
            p1 = Patient(
                name="Aarav Menon",
                age=34,
                condition="Hypertension",
                medication="Amlodipine 5mg",
                next_appointment="20 March 2026",
                doctor_id=1
            )
            p2 = Patient(
                name="Ananya Sharma",
                age=28,
                condition="Type 2 Diabetes",
                medication="Metformin 500mg",
                next_appointment="18 March 2026",
                doctor_id=2
            )
            db.session.add_all([p1, p2])
            db.session.commit()

    app.run(host="0.0.0.0", port="5000", debug=True)