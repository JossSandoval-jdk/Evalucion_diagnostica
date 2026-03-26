from flask import Blueprint, request
from drivers.controlador_horarios import (
    get_horarios,
    create_horario,
    update_horario,
    delete_horario
)

horario_bp = Blueprint('horario', __name__)

@horario_bp.route("/", methods=["GET"])
def listar_horarios():
    return get_horarios()

@horario_bp.route("/create", methods=["POST"])
def crear_horario():
    data = request.get_json()

    return create_horario(
        data["diaSemana"],
        data["h_inicio"],
        data["h_fin"],
        data["idMedico"]
    )

@horario_bp.route("/update/<int:idHorario>", methods=["PUT"])
def actualizar_horario(idHorario):
    data = request.get_json()

    return update_horario(
        idHorario,
        data["diaSemana"],
        data["h_inicio"],
        data["h_fin"]
    )

@horario_bp.route("/delete/<int:idHorario>", methods=["DELETE"])
def eliminar_horario(idHorario):
    return delete_horario(idHorario)