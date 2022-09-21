from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Password#1234@localhost:3306/hospital'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    problems = db.Column(db.String(120), nullable=False)
    contact_number = db.Column(db.BigInteger(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bed_type = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    aadhaar_number = db.Column(db.BigInteger(), nullable=False)


@app.route('/')
def index():
    patients = Patients.query.all()
    return render_template('index.html', patients=patients)


@app.route('/<int:id>/')
def patient_id(id):
    patient = Patients.query.get_or_404(id)
    return render_template('patient_id.html', patient=patient)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        problems = request.form['problems']
        contact_number = int(request.form['contact_number'])
        age = int(request.form['age'])
        bed_type = request.form['bed_type']
        address = request.form['address']
        state = request.form['state']
        city = request.form['city']
        status = request.form['status']
        problems = request.form['problems']
        aadhaar_number=request.form['aadhaar_number']
        new_Patients = Patients(name=name, problems=problems, contact_number=contact_number, age=age, bed_type=bed_type,
                                address=address, state=state, city=city, status=status, aadhaar_number=aadhaar_number)
        db.session.add(new_Patients)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    patient = Patients.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form['name']
        problems = request.form['problems']
        contact_number = int(request.form['contact_number'])
        age = int(request.form['age'])
        bed_type = request.form['bed_type']
        address = request.form['address']
        state = request.form['state']
        city = request.form['city']
        status = request.form['status']
        problems = request.form['problems']
        aadhaar_number=request.form["aadhaar_number"]

        patient.name = name
        patient.problems = problems
        patient.contact_number = contact_number
        patient.age = age
        patient.bed_type = bed_type
        patient.address = address
        patient.state = state
        patient.city = city
        patient.status = status
        patient.problems = problems
        patient.aadhaar_number=aadhaar_number

        db.session.add(patient)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', patient=patient)


@app.post('/<int:id>/delete/')
def delete(id):
    patient = Patients.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('index'))


port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(port=port)
