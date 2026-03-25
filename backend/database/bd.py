import psycopg2

def get_connection():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="Eva_Dig",
            user="postgres",
            password="josisan3108",
            port="5432"
        )
        return conexion
    except Exception as e:
        print("Error al conectar:", e)
        return None