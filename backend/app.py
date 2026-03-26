from flask import Flask

# Importar blueprints
from routes.route_medico import medico_bp
from routes.route_paciente import paciente_bp
from routes.route_especialidad import especialidad_bp
from routes.route_horarios import horario_bp
from routes.route_cita import cita_bp


def create_app():
    app = Flask(__name__)

    # 🔹 Registrar blueprints con prefijos (nombre base de URL)
    app.register_blueprint(medico_bp, url_prefix="/api/medicos")
    app.register_blueprint(paciente_bp, url_prefix="/api/pacientes")
    app.register_blueprint(especialidad_bp, url_prefix="/api/especialidades")
    app.register_blueprint(horario_bp, url_prefix="/api/horarios")
    app.register_blueprint(cita_bp, url_prefix="/api/citas")

    return app