from flask import Blueprint
from drivers.controlador_medico import get_medicos

medico_bp = Blueprint('medico', __name__)

@medico_bp.route("/medicos", methods=["GET"])
def listar_medicos():
    return get_medicos()