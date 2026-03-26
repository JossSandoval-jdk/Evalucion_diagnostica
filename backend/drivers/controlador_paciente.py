from database.bd import get_connection
from flask import jsonify

def get_pacientes():
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM PACIENTE")
    data = cursor.fetchall()

    resultado = []

    for fila in data:
        resultado.append({
            'idPaciente': fila[0],
            'nombPaciente': fila[1],
            'apePatPaciente': fila[2],
            'apeMatPaciente': fila[3],
            'sexo': fila[4],
            'direccion': fila[5],
            'email': fila[6],
            'dni': fila[7],
            'idUsuario': fila[8]
        })

    cursor.close()
    conexion.close()

    return jsonify(resultado), 200

def create_paciente(codigo, password, nombPaciente, apePatPaciente, apeMatPaciente, sexo, direccion, email, dni):
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
            INSERT INTO PACIENTE 
            (nombPaciente, apePatPaciente, apeMatPaciente, sexo, direccion, email, dni, idUsuario)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (nombPaciente, apePatPaciente, apeMatPaciente, sexo, direccion, email, dni, idUsuario))
        
        conexion.commit()
        return jsonify({"mensaje": "Paciente creado"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conexion.close()


def update_paciente(idPaciente, nombPaciente, apePatPaciente, apeMatPaciente, sexo, direccion, email, dni):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("""
            UPDATE PACIENTE 
            SET nombPaciente=%s,
                apePatPaciente=%s,
                apeMatPaciente=%s,
                sexo=%s,
                direccion=%s,
                email=%s,
                dni=%s
            WHERE idPaciente=%s
        """, (nombPaciente, apePatPaciente, apeMatPaciente, sexo, direccion, email, dni, idPaciente))
        
        conexion.commit()
        if cursor.rowcount == 0:
            return jsonify({"mensaje": "No existe"}), 404
        return jsonify({"mensaje": "Paciente actualizado"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conexion.close()


def delete_paciente(idPaciente):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("DELETE FROM PACIENTE WHERE idPaciente=%s", (idPaciente,))
        conexion.commit()

        if cursor.rowcount == 0:
            return jsonify({"mensaje": "No existe"}), 404
        
        return jsonify({"mensaje": "Eliminado"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conexion.close()