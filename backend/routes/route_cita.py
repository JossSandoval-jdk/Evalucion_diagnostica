from flask import Blueprint, request
from drivers.controlador_cita import (
    get_citas,
    create_cita,
    update_cita,
    delete_cita
)

cita_bp = Blueprint('cita', __name__)

@cita_bp.route("/", methods=["GET"])
def listar_citas():
    return get_citas()

@cita_bp.route("/create", methods=["POST"])
def crear_cita():
    data = request.get_json()

    return create_cita(
        data["f_cita"],
        data["h_cita"],
        data["estadoCita"],
        data["idMedico"],
        data["idPaciente"],
        data["idEspecialidad"]
    )

@cita_bp.route("/update/<int:idCita>", methods=["PUT"])
def actualizar_cita(idCita):
    data = request.get_json()

    return update_cita(
        idCita,
        data["estadoCita"]
    )

@cita_bp.route("/delete/<int:idCita>", methods=["DELETE"])
def eliminar_cita(idCita):
    return delete_cita(idCita)