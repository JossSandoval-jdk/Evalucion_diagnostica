const API = "/api";

let especialidades = [];
let medicos = [];
let horarios = [];
let pacientes = [];

function initCitas() {
    Promise.all([
        fetch(`${API}/especialidades/`).then(r => r.json()),
        fetch(`${API}/pacientes/`).then(r => r.json())
    ]).then(([esp, pac]) => {
        especialidades = esp || [];
        pacientes = pac || [];

        populateEspecialidades();
        populatePacientes();
        // inicial llenar medicos/horarios según primera especialidad
        handleEspecialidadChange();
    }).catch(err => {
        console.error('Error initCitas:', err);
        alert('Error cargando datos iniciales. Revisa la consola.');
    });

    document.getElementById('especialidadSelect').addEventListener('change', handleEspecialidadChange);
    document.getElementById('medicoSelect').addEventListener('change', handleMedicoChange);
    document.getElementById('btnCrear').addEventListener('click', crearCita);
}

function populateEspecialidades() {
    const sel = document.getElementById('especialidadSelect');
    sel.innerHTML = '';
    especialidades.forEach(e => {
        const opt = document.createElement('option');
        opt.value = e.idEspecialidad || e.id || e.ID || e.id_especialidad || e.IDESPECIALIDAD;
        opt.textContent = e.nombEspecialidad || e.nombre || e.nombre_especialidad || e.NOMBESPECIALIDAD;
        sel.appendChild(opt);
    });
}

function populatePacientes() {
    const sel = document.getElementById('pacienteSelect');
    sel.innerHTML = '';
    pacientes.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p.idPaciente || p.id || p.ID || p.id_paciente || p.IDPACIENTE;
        opt.textContent = `${p.nombPaciente || p.nombres || ''} ${p.apePatPaciente || ''}`;
        sel.appendChild(opt);
    });
}

function handleEspecialidadChange() {
    const espId = document.getElementById('especialidadSelect').value;
    const medSel = document.getElementById('medicoSelect');
    // si no hay especialidad seleccionada, limpiar y salir
    const horSel = document.getElementById('horarioSelect');
    if (!espId) {
        medSel.innerHTML = '<option value="">-- Seleccione especialidad --</option>';
        horSel.innerHTML = '<option value="">-- --</option>';
        return;
    }

    // pedir al backend médicos y sus horarios por especialidad
    medSel.innerHTML = '<option value="">Cargando médicos...</option>';
    horSel.innerHTML = '<option value="">-- --</option>';

    fetch(`${API}/medicos/especialidad/${espId}`)
        .then(r => r.json())
        .then(list => {
            medicos = list || [];
            medSel.innerHTML = '';
            if (!medicos.length) {
                medSel.innerHTML = '<option value="">-- No hay médicos para esta especialidad --</option>';
                horSel.innerHTML = '<option value="">-- --</option>';
                return;
            }

            medicos.forEach(m => {
                const opt = document.createElement('option');
                opt.value = m.idMedico || m.id || '';
                opt.textContent = `${m.nombMedico || ''} ${m.apePatMedico || ''}`;
                medSel.appendChild(opt);
            });
            // seleccionar el primer médico automáticamente y mostrar sus horarios
            medSel.selectedIndex = 0;
            handleMedicoChange();
        })
        .catch(err => {
            console.error('Error al cargar médicos por especialidad:', err);
            alert('Error al cargar médicos. Revisa la consola.');
        });
}

function handleMedicoChange() {
    const medId = document.getElementById('medicoSelect').value;
    const horSel = document.getElementById('horarioSelect');
    horSel.innerHTML = '';
    // buscar en el array de medicos (cada medico tiene .horarios)
    const medico = medicos.find(m => String(m.idMedico || m.id) === String(medId));
    if (!medico) {
        horSel.innerHTML = '<option value="">-- Seleccione médico --</option>';
        return;
    }
    const filtrados = medico.horarios || [];
    if (!filtrados.length) {
        horSel.innerHTML = '<option value="">-- Sin horarios disponibles --</option>';
        return;
    }
    filtrados.forEach(h => {
        const opt = document.createElement('option');
        opt.value = h.idHorario || h.id || '';
        opt.textContent = `${h.diaSemana || ''} ${h.h_inicio || ''}-${h.h_fin || ''}`;
        horSel.appendChild(opt);
    });
}

function crearCita() {
    const espId = document.getElementById('especialidadSelect').value;
    const medId = document.getElementById('medicoSelect').value;
    const pacId = document.getElementById('pacienteSelect').value;
    const fecha = document.getElementById('f_cita').value;
    const hora = document.getElementById('h_cita').value;
    const estado = document.getElementById('estadoCita').value;

    if (!fecha || !hora || !medId || !pacId || !espId) {
        alert('Complete fecha, hora, especialidad, médico y paciente');
        return;
    }

    const payload = {
        f_cita: fecha,
        h_cita: hora,
        estadoCita: estado,
        idMedico: medId,
        idPaciente: pacId,
        idEspecialidad: espId
    };

    fetch(`${API}/citas/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    }).then(res => {
        if (res.ok) {
            alert('Cita creada');
        } else {
            alert('Error al crear cita');
        }
    });
}

// inicializar cuando se cargue la página
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCitas);
} else {
    initCitas();
}
