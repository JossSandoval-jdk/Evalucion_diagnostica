from flask import Blueprint, request
from drivers.controlador_especialidad import (
    get_especialidades,
    create_especialidad,
    update_especialidad,
    delete_especialidad
)

especialidad_bp = Blueprint('especialidad', __name__)

@especialidad_bp.route("/", methods=["GET"])
def listar_especialidades():
    return get_especialidades()

@especialidad_bp.route("/create", methods=["POST"])
def crear_especialidad():
    data = request.get_json()
    return create_especialidad(data["nombEspecialidad"])

@especialidad_bp.route("/update/<int:idEspecialidad>", methods=["PUT"])
def actualizar_especialidad(idEspecialidad):
    data = request.get_json()
    return update_especialidad(idEspecialidad, data["nombEspecialidad"])

@especialidad_bp.route("/delete/<int:idEspecialidad>", methods=["DELETE"])
def eliminar_especialidad(idEspecialidad):
    return delete_especialidad(idEspecialidad)