from database.bd import get_connection
from flask import jsonify
from datetime import datetime

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

    return jsonify(resultado), 200

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
        # intentar obtener el id del médico recién creado (si la BD lo soporta)
        try:
            cursor.execute("SELECT currval(pg_get_serial_sequence('MEDICO','idMedico'))")
            idMedico = cursor.fetchone()[0]
        except Exception:
            idMedico = None

        return jsonify({"mensaje": "Médico creado correctamente", "idMedico": idMedico}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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
        if cursor.rowcount == 0:
            return jsonify({"mensaje": "No se encontró el médico"}), 404

        return jsonify({"mensaje": "Médico actualizado correctamente"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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
            return jsonify({"mensaje": "No se encontró el médico"}), 404
        
        return jsonify({"mensaje": "Médico eliminado correctamente"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conexion.close()


def get_medicos_con_horarios_por_especialidad(idEspecialidad):
    conexion = get_connection()
    if not conexion:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
    cursor = conexion.cursor()

    try:
        # la estructura esperada de MEDICO según los inserts es:
        # idMedico, nombMedico, apePatMedico, apeMatMedico, sexo, direccion, email, dni, idUsuario, idEspecialidad
        cursor.execute("SELECT * FROM MEDICO WHERE idEspecialidad=%s", (idEspecialidad,))
        med_data = cursor.fetchall()

        resultado = []

        for fila in med_data:
            idMedico = fila[0]
            medico = {
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
            }

            # obtener horarios para este medico
            cursor.execute("SELECT * FROM HORARIOS WHERE idMedico=%s", (idMedico,))
            hor_data = cursor.fetchall()
            horarios = []
            for h in hor_data:
                horarios.append({
                    'idHorario': h[0],
                    'diaSemana': h[1],
                    'h_inicio': str(h[2]),
                    'h_fin': str(h[3]),
                    'idMedico': h[4]
                })

            medico['horarios'] = horarios
            resultado.append(medico)

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conexion.close()


def get_horarios_por_especialidad_y_fecha(idEspecialidad, fecha_str):
    conexion = get_connection()
    if not conexion:
        return jsonify({'error': 'No se pudo conectar a la base de datos'}), 500
    cursor = conexion.cursor()

    try:
        # convertir fecha y obtener dia de la semana en texto
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        dias = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
        dia_nombre = dias[fecha.weekday()]

        # buscar horarios de médicos cuya especialidad sea la solicitada y que tengan horario ese día
        cursor.execute("""
            SELECT m.idMedico, m.nombMedico, m.apePatMedico, m.apeMatMedico, h.idHorario, h.diaSemana, h.h_inicio, h.h_fin
            FROM MEDICO m
            JOIN HORARIOS h ON m.idMedico = h.idMedico
            WHERE m.idEspecialidad = %s AND h.diaSemana = %s
            ORDER BY m.idMedico, h.h_inicio
        """, (idEspecialidad, dia_nombre))

        rows = cursor.fetchall()

        resultado = []
        current_med = None
        for r in rows:
            idMedico = r[0]
            if current_med is None or current_med['idMedico'] != idMedico:
                current_med = {
                    'idMedico': r[0],
                    'nombMedico': r[1],
                    'apePatMedico': r[2],
                    'apeMatMedico': r[3],
                    'horarios': []
                }
                resultado.append(current_med)

            current_med['horarios'].append({
                'idHorario': r[4],
                'diaSemana': r[5],
                'h_inicio': str(r[6]),
                'h_fin': str(r[7])
            })

        return jsonify({'fecha': fecha_str, 'dia': dia_nombre, 'medicos': resultado}), 200

    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conexion.close()