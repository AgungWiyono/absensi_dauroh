import sqlite3
from functools import wraps

from config import ROOT_PATH


def connector(func):
    @wraps(func)
    def _connect(*args, **kwargs):
        conn = sqlite3.connect(ROOT_PATH + "/app.db")
        conn.row_factory = sqlite3.Row

        try:
            return_value = func(conn, *args, **kwargs)
        except Exception as e:
            print(e)
            conn.rollback()
            raise
        else:
            conn.commit()
        finally:
            conn.close()

        return return_value

    return _connect


@connector
def insert_data(conn, data):
    param = [data["name"], data["member_id"], data["email"]]

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO absensi (name, member_id, email) VALUES (?, ?, ?)",
            param,
        )
    except sqlite3.Error:
        return (
            False,
            302,
            f"Peserta {data['name']} sudah pernah melakukan absen sebelumnya",
        )

    if not cursor.rowcount:
        return False, 400, "Absensi Gagal. Hubungi administrator."
    return (
        True,
        200,
        (
            f"Peserta {data['name']} dengan nomor {data['member_id']}",
            "berhasil melakukan Absensi",
        ),
    )


@connector
def get_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM absensi")
    return cursor.fetchall()


@connector
def get_uninserted_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM absensi WHERE inserted=0")
    return cursor.fetchall()


@connector
def update_status(conn, id_list):
    query = "UPDATE absensi SET inserted=1 WHERE id in (_?_)"
    query = query.replace("_?_", ", ".join(["?" for i in id_list]))
    print(query)

    cursor = conn.cursor()
    param = (id_list[0],) if len(id_list) == 1 else (id_list)
    print(param)

    cursor.execute(query, param)

    if not cursor.rowcount:
        return False
    return True
