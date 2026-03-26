CREATE TABLE USUARIO (
    idUsuario INT PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE ESPECIALIDAD (
    idEspecialidad INT PRIMARY KEY,
    nombEspecialidad VARCHAR(50) NOT NULL
);

CREATE TABLE MEDICO (
    idMedico INT PRIMARY KEY,
    nombMedico VARCHAR(50) NOT NULL,
    apePatMedico VARCHAR(30) NOT NULL,
    apeMatMedico VARCHAR(30) NOT NULL,
    sexo CHAR(1) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    dni VARCHAR(8) NOT NULL UNIQUE,
	imagen varchar(255) NOT NULL,
    idUsuario INT NOT NULL,
    idEspecialidad INT NOT NULL,

    FOREIGN KEY (idUsuario) REFERENCES USUARIO(idUsuario),
    FOREIGN KEY (idEspecialidad) REFERENCES ESPECIALIDAD(idEspecialidad)
);

CREATE TABLE PACIENTE (
    idPaciente INT PRIMARY KEY,
    nombPaciente VARCHAR(50) NOT NULL,
    apePatPaciente VARCHAR(30) NOT NULL,
    apeMatPaciente VARCHAR(30) NOT NULL,
    sexo CHAR(1) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    dni VARCHAR(8) NOT NULL UNIQUE,
    idUsuario INT NOT NULL,

    FOREIGN KEY (idUsuario) REFERENCES USUARIO(idUsuario)
);

CREATE TABLE HORARIOS (
    idHorario INT PRIMARY KEY,
    diaSemana VARCHAR(20) NOT NULL,
    h_inicio TIME NOT NULL,
    h_fin TIME NOT NULL,
    idMedico INT NOT NULL,

    FOREIGN KEY (idMedico) REFERENCES MEDICO(idMedico)
);

CREATE TABLE CITA (
    idCita INT PRIMARY KEY,
    f_cita DATE NOT NULL,
    h_cita TIME NOT NULL,
    estadoCita VARCHAR(30) NOT NULL,
    idMedico INT NOT NULL,
    idPaciente INT NOT NULL,
    idEspecialidad INT NOT NULL,

    FOREIGN KEY (idMedico) REFERENCES MEDICO(idMedico),
    FOREIGN KEY (idPaciente) REFERENCES PACIENTE(idPaciente),
    FOREIGN KEY (idEspecialidad) REFERENCES ESPECIALIDAD(idEspecialidad)
);