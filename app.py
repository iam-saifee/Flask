from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///doctor_appointment_system.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Set your secret key here
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    userEmail = db.Column(db.String(255), nullable=False)
    phoneNumber = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    doctor_quali = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patientID = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctorID = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    AppointmentDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')

@app.route('/')
def hello_world():
    doctor = Doctor(name="Vivek Kumar", doctor_quali="MD,MBBS", specialization="Neurosurgeon", password_hash="v123")
    db.session.add(doctor)
    db.session.commit()
    return render_template('index.html')

@app.route('/register')
def register_patient_form():
    return render_template('register.html')

@app.route('/register_patient', methods=['GET','POST'])
def register_patient():
    if request.method == 'POST':
        # Handle form submission and add patient to the database
        username = request.form['username']
        userEmail = request.form['userEmail']
        phoneNumber = request.form['phoneNumber']
        password = request.form['password']  # Add password field to the form
        new_patient = Patient(username=username, userEmail=userEmail, phoneNumber=phoneNumber)
        new_patient.set_password(password)  # Hash the password before saving
        db.session.add(new_patient)
        db.session.commit()
        flash('Patient registered successfully!', 'success')
        return render_template('register.html') # Redirect to the index page
    return render_template('index.html')

if __name__ == "__main__":
        app.run(debug=True)