from database.bd import get_connection
from flask import jsonify

def get_citas():
    conexion = get_connection()
    cursor = conexion.cursor()

    # traer también el nombre de la especialidad para facilitar la UI
    cursor.execute("""
        SELECT C.idCita, C.f_cita, C.h_cita, C.estadoCita, C.idMedico, C.idPaciente, C.idEspecialidad,
               E.nombEspecialidad
        FROM CITA C
        LEFT JOIN ESPECIALIDAD E ON C.idEspecialidad = E.idEspecialidad
    """)
    data = cursor.fetchall()

    resultado = []

    for fila in data:
        # convertir fechas/horas a strings serializables
        f_cita = fila[1]
        h_cita = fila[2]
        if hasattr(f_cita, 'isoformat'):
            f_cita = f_cita.isoformat()
        else:
            f_cita = str(f_cita)

        if hasattr(h_cita, 'isoformat'):
            h_cita = h_cita.isoformat()
        else:
            h_cita = str(h_cita)

        resultado.append({
            'idCita': fila[0],
            'f_cita': f_cita,
            'h_cita': h_cita,
            'estadoCita': fila[3],
            'idMedico': fila[4],
            'idPaciente': fila[5],
            'idEspecialidad': fila[6],
            'nombEspecialidad': fila[7]
        })

    cursor.close()
    conexion.close()

    return jsonify(resultado), 200


def create_cita(f_cita, h_cita, estadoCita, idMedico, idPaciente, idEspecialidad):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO CITA 
            (f_cita, h_cita, estadoCita, idMedico, idPaciente, idEspecialidad)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (f_cita, h_cita, estadoCita, idMedico, idPaciente, idEspecialidad))
        
        conexion.commit()
        return jsonify({"mensaje": "Cita creada"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conexion.close()


def update_cita(idCita, estadoCita):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("""
            UPDATE CITA 
            SET estadoCita=%s
            WHERE idCita=%s
        """, (estadoCita, idCita))
        
        conexion.commit()
        if cursor.rowcount == 0:
            return jsonify({"mensaje": "No existe"}), 404
        return jsonify({"mensaje": "Cita actualizada"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conexion.close()


def delete_cita(idCita):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("DELETE FROM CITA WHERE idCita=%s", (idCita,))
        conexion.commit()

        if cursor.rowcount == 0:
            return jsonify({"mensaje": "No existe"}), 404
        
        return jsonify({"mensaje": "Eliminado"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conexion.close()