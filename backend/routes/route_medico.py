from flask import Blueprint, request
from drivers.controlador_medico import (
    get_medicos,
    create_medico,
    update_medico,
    delete_medico
)
from flask import jsonify
from drivers.controlador_medico import get_horarios_por_especialidad_y_fecha

medico_bp = Blueprint('medico', __name__)

# GET
@medico_bp.route("/", methods=["GET"])
def listar_medicos():
    return get_medicos()


@medico_bp.route('/especialidad/<int:idEspecialidad>', methods=['GET'])
def medicos_por_especialidad(idEspecialidad):
    try:
        from drivers.controlador_medico import get_medicos_con_horarios_por_especialidad
        return get_medicos_con_horarios_por_especialidad(idEspecialidad)
    except Exception as e:
        # devolver un JSON consistente en caso de error
        return jsonify({'error': str(e)}), 500


@medico_bp.route('/especialidad/<int:idEspecialidad>/horarios', methods=['GET'])
def horarios_por_especialidad_y_fecha(idEspecialidad):
    fecha = request.args.get('fecha')
    if not fecha:
        return jsonify({'error': 'Parámetro fecha requerido (YYYY-MM-DD)'}), 400

    return get_horarios_por_especialidad_y_fecha(idEspecialidad, fecha)


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