from flask import Flask, render_template

# Importar blueprints
from routes.route_medico import medico_bp
from routes.route_paciente import paciente_bp
from routes.route_especialidad import especialidad_bp
from routes.route_horarios import horario_bp
from routes.route_cita import cita_bp

def create_app():
    # Crear app Flask y decirle dónde están los templates y archivos estáticos
    app = Flask(
        __name__,
        template_folder="../frontend/pages",  # Aquí está tu index.html
        static_folder="../frontend",     # Aquí están css/ y js/
        static_url_path='/frontend'        # exponer también bajo /frontend/* para compatibilidad
    )

    # 🔹 Registrar blueprints con prefijos (nombre base de URL)
    app.register_blueprint(medico_bp, url_prefix="/api/medicos")
    app.register_blueprint(paciente_bp, url_prefix="/api/pacientes")
    app.register_blueprint(especialidad_bp, url_prefix="/api/especialidades")
    app.register_blueprint(horario_bp, url_prefix="/api/horarios")
    app.register_blueprint(cita_bp, url_prefix="/api/citas")

    # 🔹 Ruta principal que carga tu index.html
    @app.route("/")
    def index():
        return render_template("index.html")    

    @app.route('/consultar')
    def consultar():
        return render_template('consultar.html')

    return app