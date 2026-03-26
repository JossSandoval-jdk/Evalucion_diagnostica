-- 1. ESPECIALIDADES
INSERT INTO ESPECIALIDAD (idEspecialidad, nombEspecialidad) VALUES 
(1, 'Cardiología'),
(2, 'Pediatría'),
(3, 'Dermatología'),
(4, 'Gastroenterología');

-- 2. USUARIOS (Credenciales para Médicos y Pacientes)
INSERT INTO USUARIO (idUsuario, codigo, password) VALUES 
(1, 'MED101', 'hash_pass_789'),
(2, 'MED102', 'hash_pass_456'),
(3, 'PAC201', 'pac_secret_1'),
(4, 'PAC202', 'pac_secret_2');

-- 3. MÉDICOS (Con fotos reales de stock)
INSERT INTO MEDICO (idMedico, nombMedico, apePatMedico, apeMatMedico, sexo, direccion, email, dni, imagen, idUsuario, idEspecialidad) VALUES 
(1, 'Carlos', 'Mendoza', 'Ruiz', 'M', 'Av. Salud 123, Lima', 'c.mendoza@clinicamed.com', '45678901', 'https://www.shutterstock.com/image-photo/portrait-handsome-hispanic-male-doctor-600nw-2608441611.jpg', 1, 1),
(2, 'Elena', 'Torres', 'Vidal', 'F', 'Calle Médicos 45, Surco', 'e.torres@clinicamed.com', '72345678', 'https://img.freepik.com/foto-gratis/hermosa-joven-doctora-mirando-camara-oficina_1301-7807.jpg?semt=ais_hybrid&w=740&q=80', 2, 2);

-- 4. PACIENTES
INSERT INTO PACIENTE (idPaciente, nombPaciente, apePatPaciente, apeMatPaciente, sexo, direccion, email, dni, idUsuario) VALUES 
(1, 'Juan', 'Pérez', 'García', 'M', 'Jr. Los Olivos 789', 'juan.perez@gmail.com', '12345678', 3),
(2, 'Ana', 'Sánchez', 'López', 'F', 'Av. Primavera 210', 'ana.sanchez@outlook.com', '87654321', 4);

-- 5. HORARIOS (Disponibilidad de los médicos)
INSERT INTO HORARIOS (idHorario, diaSemana, h_inicio, h_fin, idMedico) VALUES 
(1, 'Lunes', '08:00:00', '14:00:00', 1),
(2, 'Miércoles', '09:00:00', '13:00:00', 1),
(3, 'Martes', '14:00:00', '20:00:00', 2),
(4, 'Jueves', '14:00:00', '20:00:00', 2);

-- 6. CITAS (Ejemplos de citas registradas)
INSERT INTO CITA (idCita, f_cita, h_cita, estadoCita, idMedico, idPaciente, idEspecialidad) VALUES 
(1, '2026-04-10', '09:30:00', 'Pendiente', 1, 1, 1),
(2, '2026-04-11', '15:00:00', 'Confirmada', 2, 2, 2),
(3, '2026-04-15', '10:00:00', 'Pendiente', 1, 2, 1);