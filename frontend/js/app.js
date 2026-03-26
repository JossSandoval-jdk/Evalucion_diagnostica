const API = "/api";

let tablaActual = "medicos";
let datosGlobal = [];

const schemaMap = {
    medicos: {
        display: ['idMedico','nombMedico','apePatMedico','apeMatMedico','sexo','direccion','email','dni','idEspecialidad'],
        create: ['codigo','password','nombMedico','apePatMedico','apeMatMedico','sexo','direccion','email','dni','idEspecialidad']
    },
    pacientes: {
        display: ['idPaciente','nombPaciente','apePatPaciente','apeMatPaciente','sexo','direccion','email','dni'],
        create: ['codigo','password','nombPaciente','apePatPaciente','apeMatPaciente','sexo','direccion','email','dni']
    },
    especialidades: {
        display: ['idEspecialidad','nombEspecialidad'],
        create: ['nombEspecialidad']
    },
    horarios: {
        display: ['idHorario','diaSemana','h_inicio','h_fin','idMedico'],
        create: ['diaSemana','h_inicio','h_fin','idMedico']
    },
    citas: {
        display: ['idCita','f_cita','h_cita','estadoCita','idMedico','idPaciente','nombEspecialidad'],
        create: ['f_cita','h_cita','estadoCita','idMedico','idPaciente','idEspecialidad']
    }
};

const labelMap = {
    nombMedico: 'Nombre',
    apePatMedico: 'Apellido paterno',
    apeMatMedico: 'Apellido materno',
    nombPaciente: 'Nombre paciente',
    apePatPaciente: 'Apellido paterno',
    apeMatPaciente: 'Apellido materno',
    nombEspecialidad: 'Especialidad',
    diaSemana: 'Día',
    h_inicio: 'Hora inicio',
    h_fin: 'Hora fin',
    f_cita: 'Fecha',
    h_cita: 'Hora',
    estadoCita: 'Estado',
    };

    function labelFor(key) {
        if (labelMap[key]) return labelMap[key];
        return key.replace(/([A-Z])/g, ' $1').replace(/_/g, ' ').replace(/^./, s => s.toUpperCase());
    }

    function cargarDatos() {
        tablaActual = document.getElementById("tablaSelect").value;

        fetch(`${API}/${tablaActual}/`)
            .then(res => res.json())
            .then(data => {
                datosGlobal = data;
                renderTabla(data);
                renderFormulario(null);
            })
            .catch(err => console.error('Error al cargar datos:', err));
    }

    function renderTabla(data) {
        const thead = document.querySelector("#tablaDatos thead");
        const tbody = document.querySelector("#tablaDatos tbody");
        thead.innerHTML = "";
        tbody.innerHTML = "";

        const schema = schemaMap[tablaActual];
        const headers = schema.display;
        const idKey = headers.find(h => h.toLowerCase().includes('id')) || headers[0];

        thead.innerHTML = "<tr>" + headers.map(h => `<th>${labelFor(h)}</th>`).join("") + "<th>Acciones</th></tr>";

        data.forEach((row, i) => {
            let fila = "<tr>";
            headers.forEach(h => fila += `<td>${row[h] ?? ''}</td>`);
            fila += `<td>
                        <button onclick="editarIndex(${i})">Editar</button>
                        <button onclick="eliminar(${row[idKey]})">Eliminar</button>
                     </td>`;
            fila += "</tr>";
            tbody.innerHTML += fila;
        });
    }

    function renderFormulario(obj) {
        const form = document.getElementById("formulario");
        form.innerHTML = "";

        const schema = schemaMap[tablaActual];
        const fields = schema.create;

        const modalTitle = document.getElementById('modalTitle');
        modalTitle.textContent = obj ? `Editar ${tablaActual}` : `Nuevo ${tablaActual}`;

        if (obj) {
            const idKey = Object.keys(obj).find(k => k.toLowerCase().includes('id'));
            if (idKey) form.appendChild(Object.assign(document.createElement('input'), { type: 'hidden', id: '_id', value: obj[idKey] }));
        }

        const grid = document.createElement('div');
        grid.className = 'form-grid';

        fields.forEach(key => {
            const value = obj ? (obj[key] ?? '') : '';
            const row = document.createElement('div');
            row.className = 'form-row';

            const label = document.createElement('label');
            label.htmlFor = key;
            label.textContent = labelFor(key);

            if (key === 'estadoCita') {
                const sel = document.createElement('select');
                sel.id = key;
                ['pendiente','confirmada','cancelada'].forEach(v=>{
                    const o = document.createElement('option'); o.value = v; o.textContent = v.charAt(0).toUpperCase()+v.slice(1); if (value===v) o.selected = true; sel.appendChild(o);
                });
                row.appendChild(label);
                row.appendChild(sel);
                grid.appendChild(row);
                return;
            }

            if (['idMedico','idPaciente','idEspecialidad'].includes(key)) {
                const sel = document.createElement('select');
                sel.id = key;
                sel.innerHTML = '<option value="">Cargando...</option>';
                row.appendChild(label);
                row.appendChild(sel);
                grid.appendChild(row);
                return;
            }

            const input = document.createElement('input');
            input.type = 'text';
            input.id = key;
            input.placeholder = labelFor(key);
            input.value = value;

            row.appendChild(label);
            row.appendChild(input);
            grid.appendChild(row);
        });

        form.appendChild(grid);

        ['idMedico','idPaciente','idEspecialidad'].forEach(rel => {
            const el = document.getElementById(rel);
            if (!el) return;
            const selectedValue = obj ? (obj[rel] ?? '') : '';
            let url = '';
            if (rel === 'idMedico') url = `${API}/medicos/`;
            if (rel === 'idPaciente') url = `${API}/pacientes/`;
            if (rel === 'idEspecialidad') url = `${API}/especialidades/`;

            fetch(url)
                .then(r=>r.json())
                .then(list=>{
                    el.innerHTML = '';
                    list.forEach(item=>{
                        const opt = document.createElement('option');
                        opt.value = item[Object.keys(item).find(k=>k.toLowerCase().includes('id'))];
                        if (rel==='idMedico') opt.textContent = `${item.nombMedico} ${item.apePatMedico}`;
                        if (rel==='idPaciente') opt.textContent = `${item.nombPaciente} ${item.apePatPaciente}`;
                        if (rel==='idEspecialidad') opt.textContent = item.nombEspecialidad;
                        if (String(opt.value) === String(selectedValue)) opt.selected = true;
                        el.appendChild(opt);
                    });
                }).catch(()=>{});
        });
    }

    function guardar() {
        const form = document.getElementById('formulario');
        const inputs = form.querySelectorAll('input, select');
        let data = {};
        let id = null;

        inputs.forEach(input => {
            if (input.id === '_id') { id = input.value; return; }
            data[input.id] = input.value;
        });

        if (id) {
            fetch(`${API}/${tablaActual}/update/${id}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            }).then(()=>cargarDatos());
        } else {
            fetch(`${API}/${tablaActual}/create`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            }).then(()=>cargarDatos());
        }
        setTimeout(()=>{
            cerrarModal();
        }, 300);
    }

    function abrirModal() {
        document.getElementById('modalOverlay').style.display = 'flex';
    }

    function cerrarModal() {
        document.getElementById('modalOverlay').style.display = 'none';
    }

    function nuevo() {
        tablaActual = document.getElementById("tablaSelect").value;
        renderFormulario(null);
        abrirModal();
    }

    function eliminar(id) {
        fetch(`${API}/${tablaActual}/delete/${id}`, { method: 'DELETE' })
            .then(()=>cargarDatos());
    }

    function editarIndex(index) {
        const obj = datosGlobal[index];
        if (!obj) return;
        renderFormulario(obj);
        abrirModal();
    }

    document.addEventListener('DOMContentLoaded', () => {
        cargarDatos();
    });