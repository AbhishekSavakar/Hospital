from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask import Flask, render_template, request, jsonify
from http import HTTPStatus
import os
from flask_migrate import Migrate
from sqlalchemy.sql import func

app = Flask(__name__)
api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:welcome$1234@localhost/Hospital'
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
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())

    @staticmethod
    def addpatients(name, problems, contact_number, age, bed_type, address, state, city, status):
        new_Patients = Patients(name=name, problems=problems, contact_number=contact_number, age=age, bed_type=bed_type, address=address,
                                state=state, city=city, status=status)
        db.session.add(new_Patients)
        db.session.commit()
        return Patients.query.all()

    @staticmethod
    def getpatients():
        data = Patients.query.all()
        return data

    @staticmethod
    def jsonpatients(data):
        patientslist = []
        for patient in data:
            patientslist.append(
                {"name": patient.name, "problems": patient.problems, "contact_number":patient.contact_number,
                 "age": patient.age, "bed_type": patient.bed_type,"address": patient.address, "state": patient.state,
                 "city": patient.city,"status": patient.status, })
        return jsonify((patientslist), {"status": HTTPStatus.OK})

    @staticmethod
    def workreducer(data):
        if data:
            patientslist = []
            patientslist.append(
                {"name": data.name, "problems": data.problems, "contact_number":data.contact_number, "age": data.age,
                 "bed_type": data.bed_type, "address": data.address, "state": data.state, "city": data.city,
                 "status": data.status})
            return jsonify((patientslist), {"status": HTTPStatus.OK})
        else:
            return {"message": "Not Found", 'status': HTTPStatus.NOT_FOUND}

    @staticmethod
    def workreducerloop(data):
        if data:
            patientslist = []
            for patient in data:
                patientslist.append({"name": patient.name, "problems": patient.problems,"contact_number":patient.contact_number, "age": patient.age,
                                     "bed_type": patient.bed_type,
                                     "address": patient.address, "state": patient.state, "city": patient.city,
                                     "status": patient.status})
            return jsonify((patientslist), {"status": HTTPStatus.OK})
        else:
            return {"message": "ID Not Found", 'status': HTTPStatus.NOT_FOUND}

    @staticmethod
    def filterbypatientsid(ids):
        data = Patients.query.filter_by(id=ids).first()
        return Patients.workreducer(data)

    @staticmethod
    def filterbypatientsname(name):
        data = Patients.query.filter_by(name=name).first()
        return Patients.workreducer(data)

    @staticmethod
    def filterbyproblems(problems):
        data = Patients.query.filter_by(problems=problems).all()
        return Patients.workreducerloop(data)

    @staticmethod
    def deletebyid(ids):
        Patients.query.filter_by(id=ids).delete()
        db.session.commit()
        data = Patients.query.all()
        return Patients.workreducerloop(data)

    @staticmethod
    def updatepatients(ids):
        Patients.query.filter_by(id=ids).update(request.get_json())
        db.session.commit()
        data = Patients.query.all()
        return Patients.workreducerloop(data)


class AllPatientss(Resource):
    def post(self):
        data = request.get_json()
        data = Patients.addpatients(name=data["name"], problems=data["problems"],contact_number=data["contact_number"],
                                    age=data["age"], bed_type=data["bed_type"],address=data["address"],
                                    state=data["state"], city=data["city"],status=data["status"])
        odata = Patients.jsonpatients(data)
        return odata

    def get(self):
        data = Patients.getpatients()
        odata = Patients.jsonpatients(data)
        return odata


class OnePatientsid(Resource):
    def get(self, ids):
        data = Patients.filterbypatientsid(ids)
        return data

    def delete(self, ids):
        data = Patients.deletebyid(ids)
        return data

    def put(self, ids):
        data = Patients.updatepatients(ids)
        return data


class OnePatientstitle(Resource):
    def get(self, name):
        data = Patients.filterbypatientsname(name=name)
        return data


class GenrePatientss(Resource):
    def get(self, problems):
        data = Patients.filterbyproblems(problems)
        return data


@app.route('/')
def home():
    return render_template('home.html')


api.add_resource(AllPatientss, "/patients")
api.add_resource(OnePatientsid, "/patients/<int:ids>")
api.add_resource(OnePatientstitle, "/patients/<string:name>")
api.add_resource(GenrePatientss, "/patientsby/<string:problems>")

port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(port=port)

"""
{
    "name": "Richard",
    "problems": "Panic attack",
    "age": 27,
    "bed_type": "General",
    "address": "Silicon Valley",
    "state": "Silicon Valley",
    "city": "Silicon Valley",
    "status": "Active",
    "contact_number": 9035400190
}
"""