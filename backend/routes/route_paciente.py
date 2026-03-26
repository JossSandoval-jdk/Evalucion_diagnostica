from flask import Blueprint, request
from drivers.controlador_paciente import (
    get_pacientes,
    create_paciente,
    update_paciente,
    delete_paciente
)

paciente_bp = Blueprint('paciente', __name__)

@paciente_bp.route("/", methods=["GET"])
def listar_pacientes():
    return get_pacientes()

@paciente_bp.route("/create", methods=["POST"])
def crear_paciente():
    data = request.get_json()

    return create_paciente(
        data["codigo"],
        data["password"],
        data["nombPaciente"],
        data["apePatPaciente"],
        data["apeMatPaciente"],
        data["sexo"],
        data["direccion"],
        data["email"],
        data["dni"]
    )

@paciente_bp.route("/update/<int:idPaciente>", methods=["PUT"])
def actualizar_paciente(idPaciente):
    data = request.get_json()

    return update_paciente(
        idPaciente,
        data["nombPaciente"],
        data["apePatPaciente"],
        data["apeMatPaciente"],
        data["sexo"],
        data["direccion"],
        data["email"],
        data["dni"]
    )

@paciente_bp.route("/delete/<int:idPaciente>", methods=["DELETE"])
def eliminar_paciente(idPaciente):
    return delete_paciente(idPaciente)