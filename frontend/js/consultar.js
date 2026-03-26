const API = '/api';

function cargarEspecialidades() {
    fetch(`${API}/especialidades/`)
        .then(r => r.json())
        .then(list => {
            const sel = document.getElementById('especialidadSelect');
            sel.innerHTML = '';
            sel.appendChild(new Option('-- Seleccione --',''));
            list.forEach(item => {
                const id = item.idEspecialidad || item[Object.keys(item).find(k=>k.toLowerCase().includes('id'))];
                sel.appendChild(new Option(item.nombEspecialidad, id));
            });

            sel.addEventListener('change', ()=>{
                if (sel.value) cargarMedicos(sel.value);
                else document.getElementById('medicosContainer').innerHTML = '';
            });
        });
}

function cargarMedicos(idEspecialidad) {
    fetch(`${API}/medicos/especialidad/${idEspecialidad}`)
        .then(r => r.json())
        .then(list => renderMedicos(list))
        .catch(err=> console.error(err));
}

function renderMedicos(list) {
    const container = document.getElementById('medicosContainer');
    container.innerHTML = '';

    if (!Array.isArray(list) || list.length === 0) {
        container.innerHTML = '<p>No hay médicos para esta especialidad.</p>';
        return;
    }

    list.forEach(m => {
        const card = document.createElement('div');
        card.className = 'card-medico';

        const img = document.createElement('img');
        img.src = m.imagen || '/frontend/css/placeholder.png' ;
        img.alt = `${m.nombMedico}`;

        const info = document.createElement('div');
        info.innerHTML = `<strong>${m.nombMedico || ''} ${m.apePatMedico || ''} ${m.apeMatMedico || ''}</strong>
                          <div>${m.direccion || ''}</div>
                          <div>${m.email || ''}</div>`;

        const horariosDiv = document.createElement('div');
        horariosDiv.className = 'horarios-list';
        if (Array.isArray(m.horarios) && m.horarios.length) {
            const ul = document.createElement('ul');
            m.horarios.forEach(h => {
                const li = document.createElement('li');
                li.textContent = `${h.diaSemana} ${h.h_inicio} - ${h.h_fin}`;
                ul.appendChild(li);
            });
            horariosDiv.appendChild(ul);
        } else {
            horariosDiv.textContent = 'Sin horarios.';
        }

        card.appendChild(img);
        card.appendChild(info);
        card.appendChild(horariosDiv);

        container.appendChild(card);
    });
}

document.addEventListener('DOMContentLoaded', ()=>{
    cargarEspecialidades();
});