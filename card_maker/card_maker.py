import os
import sys
import csv
import base64
from io import BytesIO

import qrcode
import pdfkit
from jinja2 import Template

data = {
    "name": "Agung Wiyono",
    "kode": "DTN-01001",
    "email": "wiyonoagung1@gmail.com",
}


def card_creator(member, batch):
    data = qrcode.make(f"{member['name']}|{member['kode']}|{member['email']}")
    temp_file = BytesIO()

    data.save(temp_file)
    temp_file.seek(0)
    qrcode_text = base64.b64encode(temp_file.getvalue()).decode()

    gender = "ikhwan" if member["gender"] == "Ikhwan" else "akhwat"

    with open(f"card_dauroh_{gender}/index.html", "r") as f:
        template = Template(f.read())

    new_template = template.render(qrcode=qrcode_text, member=member)

    pdfkit.from_string(
        new_template, f"cards/batch{batch}/{member['kode']}.pdf"
    )


def path_checker(batch):
    if not os.path.isdir(f"cards/batch{batch}"):
        os.mkdir(f"cards/batch{batch}")


def csv_reader(filename, batch):
    dataset = []
    with open(filename, "r") as f:
        raw_data = csv.DictReader(f)
        for data in raw_data:
            dataset.append(data)

    path_checker(batch)

    start = 100 * (batch - 1)
    end = 100 * batch
    sliced_data = dataset[start:end]

    for record in sliced_data:
        member = {
            "name": record["Nama Lengkap"],
            "kode": record["No. Induk"],
            "email": record["Email Address"],
            "gender": record["Jenis Kelamin"],
        }
        card_creator(member, batch)


if __name__ == "__main__":
    filename = sys.argv[1]
    batch = int(sys.argv[2])
    csv_reader(filename, batch)
