from flask import request
from flask_restplus import Resource, fields

from api import api
from api import db_worker

input_model = api.model(
    "Input Model",
    {
        "name": fields.String(required=True, help="Nama Peserta"),
        "member_id": fields.String(required=True, help="Nomor Induk Peserta"),
        "email": fields.String(required=True, help="Alamat Email Peserta"),
    },
)


@api.route("/test")
class Test(Resource):
    @api.doc(body=input_model)
    def post(self):
        data = request.get_json()

        status, code, msg = db_worker.insert_data(data)
        return {"msg": msg}, code
