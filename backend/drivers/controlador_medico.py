from database.bd import get_connection
from flask import jsonify

def get_medicos():
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM MEDICO")
    data = cursor.fetchall()

    resultado = []

    for fila in data:
        resultado.append({
            'idMedico': fila[0],
            'nombMedico': fila[1],
            'apePatMedico': fila[2],
            'apeMatMedico': fila[3],
            'sexo': fila[4],
            'direccion': fila[5],
            'email': fila[6],
            'dni': fila[7],
            'idUsuario': fila[8],
            'idEspecialidad': fila[9]
        })

    cursor.close()
    conexion.close()

    return jsonify(resultado)

def create_medico(codigo, password, nombMedico, apePatMedico, apeMatMedico, sexo, direccion, email, dni, idEspecialidad):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO USUARIO (codigo, password) 
            VALUES (%s, %s) 
            RETURNING idUsuario
        """, (codigo, password))
        
        idUsuario = cursor.fetchone()[0]  
        
        cursor.execute("""
            INSERT INTO MEDICO 
            (nombMedico, apePatMedico, apeMatMedico, sexo, direccion, email, dni, idEspecialidad, idUsuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombMedico, apePatMedico, apeMatMedico, sexo, direccion, email, dni, idEspecialidad, idUsuario))
        
        conexion.commit()
        
        return {"mensaje": "Médico creado correctamente"}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        cursor.close()
        conexion.close()
def update_medico(idMedico, nombMedico, apePatMedico, apeMatMedico, sexo, direccion, email, dni, idEspecialidad):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("""
            UPDATE MEDICO 
            SET nombMedico=%s,
                apePatMedico=%s,
                apeMatMedico=%s,
                sexo=%s,
                direccion=%s,
                email=%s,
                dni=%s,
                idEspecialidad=%s 
            WHERE idMedico=%s
        """, (nombMedico, apePatMedico, apeMatMedico, sexo, direccion, email, dni, idEspecialidad, idMedico))
        
        conexion.commit()
        
        return {"mensaje": "Médico actualizado correctamente"}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        cursor.close()
        conexion.close()

def delete_medico(idMedico):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("DELETE FROM MEDICO WHERE idMedico=%s", (idMedico,))
        
        conexion.commit()
        
        if cursor.rowcount == 0:
            return {"mensaje": "No se encontró el médico"}
        
        return {"mensaje": "Médico eliminado correctamente"}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        cursor.close()
        conexion.close()