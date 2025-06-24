use master;
ALTER DATABASE chefhub SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
DROP DATABASE chefhub;


create database chefhub;

use chefhub;

create table usuarios(
	idUsuario int not null identity constraint pk_usuarios primary key,
	mail varchar(150) unique,
	nickname varchar(100)  not null,
	habilitado varchar(2) constraint chk_habilitado check (habilitado in ('Si','No')),
	nombre varchar(150),
	direccion varchar(150),
	avatar varchar(300) -- url de la imagen del avatar,
)

create table alumnos (
	idAlumno int not null constraint pk_alumnos primary key,
	numeroTarjeta varchar(12),
	dniFrente varchar(300), -- url de la imagen del dni
	dniFondo varchar(300), -- url de la imagen del dni
	tramite varchar(12),
    cuentaCorriente decimal(12,2),
	constraint fk_alumnos_usuarios foreign key (idAlumno) references usuarios(idUsuario)
)

create table tiposReceta(
	idTipo int not null identity constraint pk_tipos primary key,
	descripcion varchar(250)
)

create table recetas(
	idReceta int not null identity constraint pk_recetas primary key,
	idUsuario int,
	nombreReceta varchar(500),
	descripcionReceta varchar(1000),
	fotoPrincipal varchar(300), -- url de la imagen del plato, siempre tiene al menos una les demas estarán en la tabla fotos.
	porciones int,
	cantidadPersonas int,
	idTipo int,
	constraint fk_recetas_usuarios foreign key (idUsuario) references usuarios,
	constraint fk_recetas_tipos foreign key (idTipo) references tiposReceta
)


create table ingredientes( /* Esta tabla tiene los ingredientes que el usuario utiliza para cargar la receta, si el ingrediente no esta puede cargarlo - Esos ingredientes se validan cuando se aprueba la receta */
	idIngrediente int not null identity constraint pk_ingredientes primary key,
	nombre varchar(200)
)


create table unidades(
	idUnidad int not null identity constraint pk_unidades primary key,
	descripcion varchar(50) not null
)


create table utilizados (
	idUtilizado int not null identity constraint pk_utilizados primary key,
	idReceta int,
	idIngrediente int,
	cantidad int,
	idUnidad int,
	observaciones varchar(500), /*Son comentarios sobre el ingrediente*/
	constraint fk_utilizados_recetas foreign key (idReceta) references recetas,
	constraint fk_utilizados_ingredientes foreign key (idIngrediente) references ingredientes,
	constraint fk_utilizados_unidades foreign key (idUnidad) references unidades
)

create table calificaciones(
	idCalificacion int not null identity constraint pk_calificaciones primary key,
	idusuario int, /*usuario de la calificacion no de la receta*/
	idReceta int,
	calificacion int, /*Si no utiliza un valr numerico hay que cambiar el tipo*/
	comentarios varchar(500),
	constraint fk_calificaciones_usuarios foreign key (idUsuario) references usuarios,
	constraint fk_calificaciones_recetas foreign key (idReceta) references recetas
)


create table conversiones(
	idConversion int not null identity constraint pk_conversiones primary key,
	idUnidadOrigen int not null,
	idUnidadDestino int not null,
	factorConversiones float,
	constraint fk_unidad_origen foreign key (idUnidadOrigen) references unidades (idUnidad),
	constraint fk_unidad_destino foreign key (idUnidadDestino) references unidades (idUnidad)
)

create table pasos(
	idPaso int not null identity constraint pk_pasos primary key,
	idReceta int,
	nroPaso int,
	texto varchar(4000),
	constraint fk_pasos_recetas foreign key (idReceta) references recetas
)


create table fotos(
	idfoto int not null identity constraint pk_fotos primary key,
	idReceta int not null,
	urlFoto varchar(300),
	extension varchar(5),
	constraint fk_fotos_recetas foreign key (idReceta) references recetas
)


create table multimedia(
	idContenido int not null identity constraint pk_multimedia primary key,
	idPaso int not null,
	tipo_contenido varchar(10) constraint chk_tipo_contenido check (tipo_contenido in ('foto','video','audio')),
	extension varchar(5),
	urlContenido varchar(300),
	constraint fk_multimedia_pasos foreign key (idPaso) references pasos
)

create table sedes(
    idSede int not null identity constraint pk_sedes primary key,
    nombreSede varchar(150) not null,
    direccionSede varchar(250) not null,
    telefonoSede varchar(15),
    mailSede varchar(150),
    whatsApp varchar(15),
    tipoBonificacion varchar(20),
    bonificacionCursos decimal(10,2),
    tipoPromocion varchar(20),
    promocionCursos decimal(10,2)
)


create table cursos(
    idCurso int not null identity constraint pk_cursos primary key, 
    descripcion varchar(300),
    contenidos varchar(500),
    requerimientos varchar(500),
    duracion int,
    precio decimal(12,2), 
    modalidad varchar(20) constraint chk_tipo_curso check (modalidad in ('presencial','remoto','virtual'))
)


create table cronogramaCursos(
    idCronograma int not null identity constraint pk_cronogramaCursos primary key, 
    idSede int not null,
    idCurso int not null,
    fechaInicio date,
    fechaFin date, 
    vacantesDisponibles int,
    constraint fk_cronogramaCursos_sedes foreign key (idSede) references sedes,
    constraint fk_cronogramaCursos_cursos foreign key (idCurso) references cursos
) 

create table asistenciaCursos(
    idAsistencia int not null identity constraint pk_asistenciaCursos primary key, 
    idAlumno int not null,
    idCronograma int not null,
    fecha datetime,
    constraint fk_asistenciaCursos_alumnos foreign key (idAlumno) references alumnos,
    constraint fk_asistenciaCursos_cronograma foreign key (idCronograma) references cronogramaCursos
)



/*EXTRAS*/

create table passwords(
idpassword int not null constraint pk_passwords primary key, -- FK hacia usuarios.idUsuario
password varchar(255) not null,
constraint fk_passwords_usuarios foreign key (idpassword) references usuarios(idUsuario)
);


CREATE TABLE estadoReceta (
    idEstado INT NOT NULL IDENTITY CONSTRAINT pk_estadoReceta PRIMARY KEY,
    idReceta INT NOT NULL,
    estado VARCHAR(50) NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT fk_estadoReceta_receta FOREIGN KEY (idReceta) REFERENCES recetas(idReceta)
);

CREATE TABLE estadoComentario(
    idEstadoComentario INT NOT NULL IDENTITY CONSTRAINT pk_idEstadoComentario PRIMARY KEY,
    idCalificacion INT NOT NULL,
    estado varchar(20) not null,
    fechaEstado DATETIME NOT NULL DEFAULT GETDATE(),
    observaciones VARCHAR(50) NOT NULL,
    CONSTRAINT fk_idCalificacion FOREIGN KEY (idCalificacion) REFERENCES calificaciones(idCalificacion)
);

CREATE TABLE recetasFavoritas (
    idCreador INT NOT NULL,
    idReceta INT NOT NULL,
    CONSTRAINT pk_recetasFavoritas PRIMARY KEY (idCreador, idReceta),
    CONSTRAINT fk_recetasFavoritas_usuarios FOREIGN KEY (idCreador) REFERENCES usuarios(idUsuario),
    CONSTRAINT fk_recetasFavoritas_recetas FOREIGN KEY (idReceta) REFERENCES recetas(idReceta)
);


CREATE TABLE notificaciones (
    idNotificacion INT NOT NULL IDENTITY CONSTRAINT pk_idNotificacion PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    idUsuario int not null,
    fecha_envio DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT fk_idUsuario_usuario FOREIGN KEY (idUsuario) REFERENCES usuarios(idUsuario)
);

--create table fotosCursos(
--	idfoto int not null identity constraint pk_fotos primary key,
--	idCurso int not null,
--	urlFoto varchar(300),
--	extension varchar(5),
--	constraint fk_fotos_recetas foreign key (idCurso) references cursos
--)


--create table fotosSedes(
--	idfoto int not null identity constraint pk_fotos primary key,
--	idSede int not null,
--	urlFoto varchar(300),
--	extension varchar(5),
--	constraint fk_fotos_recetas foreign key (idSede) references sedes
--)


