from database.bd import get_connection
from flask import jsonify

def get_citas():
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM CITA")
    data = cursor.fetchall()

    resultado = []

    for fila in data:
        resultado.append({
            'idCita': fila[0],
            'f_cita': fila[1],
            'h_cita': fila[2],
            'estadoCita': fila[3],
            'idMedico': fila[4],
            'idPaciente': fila[5],
            'idEspecialidad': fila[6]
        })

    cursor.close()
    conexion.close()

    return jsonify(resultado)


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
        return {"mensaje": "Cita creada"}
    
    except Exception as e:
        return {"error": str(e)}
    
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
        return {"mensaje": "Cita actualizada"}
    
    except Exception as e:
        return {"error": str(e)}
    
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
            return {"mensaje": "No existe"}
        
        return {"mensaje": "Eliminado"}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        cursor.close()
        conexion.close()