from database.bd import get_connection
from flask import jsonify

def get_especialidades():
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM ESPECIALIDAD")
    data = cursor.fetchall()

    resultado = []

    for fila in data:
        resultado.append({
            'idEspecialidad': fila[0],
            'nombEspecialidad': fila[1]
        })

    cursor.close()
    conexion.close()

    return jsonify(resultado)


def create_especialidad(nombEspecialidad):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO ESPECIALIDAD (nombEspecialidad) VALUES (%s)",
            (nombEspecialidad,)
        )
        conexion.commit()
        return {"mensaje": "Especialidad creada"}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        cursor.close()
        conexion.close()


def update_especialidad(idEspecialidad, nombEspecialidad):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.execute(
            "UPDATE ESPECIALIDAD SET nombEspecialidad=%s WHERE idEspecialidad=%s",
            (nombEspecialidad, idEspecialidad)
        )
        conexion.commit()
        return {"mensaje": "Especialidad actualizada"}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        cursor.close()
        conexion.close()


def delete_especialidad(idEspecialidad):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("DELETE FROM ESPECIALIDAD WHERE idEspecialidad=%s", (idEspecialidad,))
        conexion.commit()

        if cursor.rowcount == 0:
            return {"mensaje": "No existe"}
        
        return {"mensaje": "Eliminado"}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        cursor.close()
        conexion.close()