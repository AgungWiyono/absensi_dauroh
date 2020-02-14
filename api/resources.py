from flask import request, render_template
from flask_restplus import Resource, fields

from api import app, api
from api import db_worker

input_model = api.model(
    "Input Model",
    {
        "name": fields.String(required=True, help="Nama Peserta"),
        "member_id": fields.String(required=True, help="Nomor Induk Peserta"),
        "email": fields.String(required=True, help="Alamat Email Peserta"),
    },
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scan')
def scan():
    return render_template('instascan.html')


@app.route('/test-scan')
def test_scan():
    return render_template('test_scan.html')


@api.route("/test")
class Test(Resource):
    @api.doc(body=input_model)
    def post(self):
        data = request.get_json()

        status, code, msg = db_worker.insert_data(data)

        return {"msg": msg}, code
