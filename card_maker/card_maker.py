import os
import csv
import base64
from io import BytesIO

import qrcode
import pdfkit
from jinja2 import Template

from card_maker import CARD_MAKER_CONFIG, BASE_DIR

data = {
    "name": "Agung Wiyono",
    "kode": "DTN-01001",
    "email": "wiyonoagung1@gmail.com",
}

TEMPLATE_FOLDER = {
    "Ikhwan": BASE_DIR + "/card_dauroh_ikhwan",
    "Akhawat": BASE_DIR + "/card_dauroh_akhwat",
}


def card_creator(member, batch):
    data = qrcode.make(f"{member['name']}|{member['kode']}|{member['email']}")
    temp_file = BytesIO()

    data.save(temp_file)
    temp_file.seek(0)
    qrcode_text = base64.b64encode(temp_file.getvalue()).decode()

    with open(TEMPLATE_FOLDER[member["gender"]] + "/index.html", "r") as f:
        template = Template(f.read())

    new_template = template.render(
        qrcode=qrcode_text,
        member=member,
        path=TEMPLATE_FOLDER[member["gender"]],
    )

    pdfkit.from_string(
        new_template,
        CARD_MAKER_CONFIG["saved_card_folder"]
        + f"cards/batch{batch}/{member['kode']}.pdf",
    )


def path_checker(batch):
    if not os.path.isdir(
        CARD_MAKER_CONFIG["saved_card_folder"] + f"cards/batch{batch}"
    ):
        os.mkdir(
            CARD_MAKER_CONFIG["saved_card_folder"] + f"cards/batch{batch}"
        )


def csv_reader(batch):
    dataset = []
    with open(CARD_MAKER_CONFIG["source_file"], "r") as f:
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
