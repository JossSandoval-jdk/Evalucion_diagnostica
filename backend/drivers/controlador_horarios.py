from database.bd import get_connection
from flask import jsonify

def get_horarios():
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM HORARIOS")
    data = cursor.fetchall()

    resultado = []

    for fila in data:
        resultado.append({
            'idHorario': fila[0],
            'diaSemana': fila[1],
            'h_inicio': fila[2],
            'h_fin': fila[3],
            'idMedico': fila[4]
        })

    cursor.close()
    conexion.close()

    return jsonify(resultado)


def create_horario(diaSemana, h_inicio, h_fin, idMedico):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO HORARIOS (diaSemana, h_inicio, h_fin, idMedico)
            VALUES (%s,%s,%s,%s)
        """, (diaSemana, h_inicio, h_fin, idMedico))
        
        conexion.commit()
        return {"mensaje": "Horario creado"}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        cursor.close()
        conexion.close()


def update_horario(idHorario, diaSemana, h_inicio, h_fin):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("""
            UPDATE HORARIOS 
            SET diaSemana=%s,
                h_inicio=%s,
                h_fin=%s
            WHERE idHorario=%s
        """, (diaSemana, h_inicio, h_fin, idHorario))
        
        conexion.commit()
        return {"mensaje": "Horario actualizado"}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        cursor.close()
        conexion.close()


def delete_horario(idHorario):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("DELETE FROM HORARIOS WHERE idHorario=%s", (idHorario,))
        conexion.commit()

        if cursor.rowcount == 0:
            return {"mensaje": "No existe"}
        
        return {"mensaje": "Eliminado"}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        cursor.close()
        conexion.close()