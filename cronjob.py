from api import db_worker, spreadsheet


def write_data(data):
    values = [
        [element["name"], element["member_id"], element["email"]]
        for element in data
    ]

    status = spreadsheet.write_values(values)
    if status:
        print("Succes")
    else:
        print("Failed")


def main():
    data = [dict(i) for i in db_worker.get_uninserted_data()]

    if data:
        write_data(data)
        ids = [i["id"] for i in data]
        db_worker.update_status(ids)
    else:
        print("No Data")


if __name__ == "__main__":
    main()
