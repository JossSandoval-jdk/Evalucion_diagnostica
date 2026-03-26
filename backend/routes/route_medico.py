from flask import Blueprint, request
from drivers.controlador_medico import (
    get_medicos,
    create_medico,
    update_medico,
    delete_medico
)

medico_bp = Blueprint('medico', __name__)

# GET
@medico_bp.route("/", methods=["GET"])
def listar_medicos():
    return get_medicos()


#POST
@medico_bp.route("/create", methods=["POST"])
def crear_medico():
    data = request.get_json()

    return create_medico(
        data["codigo"],
        data["password"],
        data["nombMedico"],
        data["apePatMedico"],
        data["apeMatMedico"],
        data["sexo"],
        data["direccion"],
        data["email"],
        data["dni"],
        data["idEspecialidad"]
    )


#PUT
@medico_bp.route("/update/<int:idMedico>", methods=["PUT"])
def actualizar_medico(idMedico):
    data = request.get_json()

    return update_medico(
        idMedico,
        data["nombMedico"],
        data["apePatMedico"],
        data["apeMatMedico"],
        data["sexo"],
        data["direccion"],
        data["email"],
        data["dni"],
        data["idEspecialidad"]
    )


#DELETE
@medico_bp.route("/delete/<int:idMedico>", methods=["DELETE"])
def eliminar_medico(idMedico):
    return delete_medico(idMedico)