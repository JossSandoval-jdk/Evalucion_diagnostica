from database.bd import get_connection
from flask import jsonify

def get_medicos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM MEDICO")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data)