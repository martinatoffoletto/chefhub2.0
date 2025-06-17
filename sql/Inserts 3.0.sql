use chefhub; 

INSERT INTO usuarios (mail, nickname, habilitado, nombre, direccion, avatar) VALUES
('ana.gomez@email.com',      'ana123',     'Si', 'Ana Gómez',       'Av. Siempre Viva 123', 'img/cocinero1.png'),
('lucas.rojas@email.com',    'lucasr',     'Si', 'Lucas Rojas',     'Calle Falsa 456', 'img/cocinero1.png'),
('maria.lopez@email.com',    'marial',     'Si', 'María López',     'Pasaje Las Rosas 789', 'img/cocinero1.png'),
('juan.perez@email.com',     'jperez',     'Si', 'Juan Pérez',      'Ruta 5 Km 23', 'img/cocinero1.png'),
('carla.diaz@email.com',     'carlad',     'Si', 'Carla Díaz',      'Av. Libertador 1001', 'img/cocinero1.png'),
('martin.sosa@email.com',    'msosa89',    'Si', 'Martín Sosa',     'Calle 9 de Julio 234', 'img/cocinero1.png'),
('sofia.fernandez@email.com','sofi_fz',    'Si', 'Sofía Fernández', 'Diagonal Norte 321', 'img/cocinero1.png'),
('diego.martinez@email.com', 'diegom',     'Si', 'Diego Martínez',  'Boulevard Mitre 12', 'img/cocinero1.png'),
('paula.mendez@email.com',    'paulam',    'Si', 'Paula Méndez',    'Av. Córdoba 1234', 'img/cocinero1.png'),
('fernando.castro@email.com', 'fercast',   'Si', 'Fernando Castro', 'Calle Belgrano 567', 'img/cocinero1.png'),
('laura.ramos@email.com',     'laurar',    'Si', 'Laura Ramos',     'Paseo Colon 890', 'img/cocinero1.png'),
('diego.torres@email.com',    'dtorres',   'Si', 'Diego Torres',    'Av. San Martin 234', 'img/cocinero1.png'),
('carolina.vazquez@email.com','carovaz',   'Si', 'Carolina Vázquez','Boulevard Oroño 45', 'img/cocinero1.png');


INSERT INTO alumnos (idAlumno, numeroTarjeta, dniFrente, dniFondo, tramite, cuentaCorriente) VALUES
(1, '123456789012', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000001', 0.50),
(2, '234567890123', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000002', 2450.00),
(3, '345678901234', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000003', 0.00), -- los casos donde esta en 0, es porque estan al dia con los pagos de los cursos
(4, '456789012345', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000004', 1800.00),
(5, '567890123456', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000005', 500.25),
(6, '678901234567', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000006', 0.00),
(7, '789012345678', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000007', 1750.80),
(8, '890123456789', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000008', 0.00);

INSERT INTO tiposReceta (descripcion) VALUES
('Postres y dulces'),
('Entrantes y aperitivos'),
('Platos principales'),
('Ensaladas'),
('Sopas y cremas'),
('Bebidas'),
('Salsas y aderezos'),
('Panadería y repostería');

INSERT INTO recetas (idUsuario, nombreReceta, descripcionReceta, fotoPrincipal, porciones, cantidadPersonas, idTipo) VALUES
(1, 'Lasaña vegetariana de berenjenas', 'Una receta nutritiva y sabrosa de lasaña sin carne, con capas de berenjena, ricotta y salsa de tomate casera.', 'img/rBerenjena.jpg', 8, 4, 3),
(1, 'Cous cous con vegetales', 'Una comida rápida, sabrosa y colorida con verduras salteadas.', 'img/cousCousveg.jpg', 4, 2, 4),
(2, 'Rissotto', 'Rissotto cremoso y reconfortante para clima frio.', 'img/rRisotto.jpg', 6, 3, 5),
(2, 'Pan casero', 'Pan artesanal con corteza crujiente y miga suave.', 'rPanArtesanal.jpg', 1, 10, 8),
(3, 'Mousse de chocolate', 'Postre ligero y esponjoso de chocolate amargo.', 'img/mousseChoco.jpg', 6, 6, 1),
(4, 'Cheescake de Frutilla', 'Tarta fría con base de galletitas y relleno de queso crema, cubierta con salsa de frutillas frescas.', 'img/rBerenjena.jpg', 1, 8, 1),
(4, 'Ensalada tibia de lentejas', 'Una ensalada nutritiva y reconfortante con lentejas, zanahoria, cebolla morada y un toque de limón.', 'img/rBerenjena.jpg', 2, 2, 4),
(3, 'Empanadas salteñas', 'Empanadas argentinas tradicionales con carne jugosa, cebolla, huevo y especias de Salta.', 'img/rEmpanadasCarne.jpg', 12, 6, 3);

INSERT INTO ingredientes (nombre) VALUES
('Cous Cous'),
('Carne'),
('Harina'),
('Aceite de oliva'),
('Cebolla'),
('Huevo'),
('Vegetales'),
('Chocolate'),
('Frutillas'),
('Levadura'),
('Berenjena'),
('Ricota'),
('Salsa de Tomate'),
('Morron'),
('Ajo'),
('Huevos'),
('Lentejas'),
('Arroz');

INSERT INTO unidades (descripcion) VALUES
('g'),
('kg'),
('ml'),
('l'),
('taza');

INSERT INTO utilizados (idReceta, idIngrediente, cantidad, idUnidad, observaciones) VALUES
(1, 11, 500, 1, 'Rodajas para capas'),
(1, 12, 300, 1, 'Ricota para relleno'),
(1, 13, 400, 3, 'Salsa de tomate casera'),
(2, 1, 200, 1, 'Cous cous cocido'),
(2, 7, 300, 1, 'Vegetales variados'),
(2, 4, 30, 3, 'Aceite de oliva para saltear'),
(3, 5, 150, 1, 'Cebolla picada'),
(3, 6, 3, 5, 'Huevos para acompañar'),
(3, 4, 20, 3, 'Aceite de oliva para sofreír'),
(4, 3, 500, 1, 'Harina para la masa'),
(4, 10, 15, 1, 'Levadura fresca'),
(4, 4, 25, 3, 'Aceite de oliva'),
(5, 8, 200, 1, 'Chocolate amargo'),
(5, 6, 3, 5, 'Huevos para la mousse'),
(5, 9, 150, 1, 'Frutillas frescas para decoración'),
(6, 3, 200, 1, 'Harina para base'),
(6, 12, 400, 1, 'Queso crema para relleno'),
(6, 9, 150, 1, 'Frutillas frescas para cobertura'),
(7, 17, 300, 1, 'Lentejas cocidas '),
(7, 5, 100, 1, 'Cebolla morada picada'),
(7, 14, 50, 1, 'Morron picado'),
(8, 2, 400, 1, 'Carne picada'),
(8, 5, 150, 1, 'Cebolla picada'),
(8, 6, 3, 5, 'Huevos para relleno y masa'); 

INSERT INTO calificaciones (idusuario, idReceta, calificacion, comentarios) VALUES -- consideramos puntuacion del 1 al 5
(1, 1, 5, 'Excelente receta, muy bien explicada y deliciosa.'),
(2, 3, 4, 'Muy buena sopa, perfecta para el invierno.'),
(3, 5, 3, 'El mousse quedó un poco dulce para mi gusto, pero rico.'),
(5, 5, 5, 'El mousse quedó muy rico.'),
(7, 1, 5, 'Receta fácil y rápida, muy buena.'),
(2, 3, 5, 'Muy rica sopa !!');

INSERT INTO conversiones (idUnidadOrigen, idUnidadDestino, factorConversiones)
VALUES 
(2, 1, 1000),   -- kg → g
(1, 2, 0.001),   -- g → kg
(4, 3, 1000),   -- l → ml
(3, 4, 0.001);  -- ml → l 


INSERT INTO pasos (idReceta, nroPaso, texto) VALUES
(1, 1, 'Cortar las berenjenas en rodajas finas y asarlas en el horno.'),
(1, 2, 'Preparar la salsa de tomate con ajo, cebolla y albahaca.'),
(1, 3, 'Armar la lasaña intercalando capas de berenjena, ricota y salsa.'),
(2, 1, 'Hidratar el cous cous con agua caliente y dejar reposar.'),
(2, 2, 'Saltear los vegetales variados con aceite de oliva.'),
(2, 3, 'Mezclar el cous cous con los vegetales salteados y condimentar.'),
(3, 1, 'Picar la cebolla y sofreír en aceite de oliva hasta dorar.'),
(3, 2, 'Agregar el caldo junto al arroz, cocinar hasta que esté tierna.'),
(3, 3, 'Procesar y servir con huevo duro picado.'),
(4, 1, 'Mezclar harina, levadura, agua y aceite para formar la masa.'),
(4, 2, 'Dejar levar la masa hasta que duplique su tamaño.'),
(4, 3, 'Hornear la masa hasta que esté dorada y crujiente.'),
(5, 1, 'Derretir el chocolate a baño maría.'),
(5, 2, 'Batir las claras a punto nieve y mezclar con el chocolate.'),
(5, 3, 'Refrigerar la mezcla hasta que tome consistencia.'),
(6, 1, 'Preparar la base mezclando harina con manteca y azúcar.'),
(6, 2, 'Batir la ricota con azúcar y agregar a la base.'),
(6, 3, 'Cubrir con salsa de frutillas y refrigerar.'),
(7, 1, 'Cocer las lentejas hasta que estén tiernas.'),
(7, 2, 'Saltear cebolla y morrón, mezclar con las lentejas.'),
(7, 3, 'Aliñar con limón y servir tibio.'),
(8, 1, 'Preparar el relleno con carne, cebolla y condimentos.'),
(8, 2, 'Rellenar las tapas de empanadas y cerrar bien.'),
(8, 3, 'Hornear hasta que estén doradas y crujientes.');

INSERT INTO fotos (idReceta, urlFoto, extension) VALUES
(1, 'img/rBerenjena.jpg', '.jpg'),
(2, 'img/cousCousveg.jpg', '.jpg'),
(3, 'img/rRisotto.jpg', '.jpg'),
(4, 'img/rPanArtesanal.jpg', '.jpg'),
(5, 'img/mousseChoco.jpg', '.jpg'),
(6, 'img/rCheesecake.jpg', '.jpg'),
(7, 'img/rLentejas.jpg', '.jpg'),
(8, 'img/rEmpanadasCarne.jpg', '.jpg');

INSERT INTO sedes (
    nombreSede, direccionSede, telefonoSede, mailSede, whatsApp, 
    tipoBonificacion, bonificacionCursos, tipoPromocion, promocionCursos
)
VALUES 
(
    'Sede Palermo',
    'Av. Santa Fe 3456, Palermo, CABA',
    '01147781234',
    'palermo@cocinaedu.ar',
    '5491167891234',
    'Descuento del 10%',
    10.00,
    'Descuento del 15%',
    15.00
),
(
    'Sede Caballito',
    'José María Moreno 789, Caballito, CABA',
    '01149231234',
    'caballito@cocinaedu.ar',
    '5491145678901',
    'Descuento del 10%',
    10.00,
    'Descuento del 10%',
    15.00
),
(
    'Sede Belgrano',
    'Av. Cabildo 2233, Belgrano, CABA',
    '01147891234',
    'belgrano@cocinaedu.ar',
    '5491176543210',
    'Descuento del 20%',
    20.00,
    'Descuento del 5%',
    5.00
);

INSERT INTO cursos (descripcion, contenidos, requerimientos, duracion, precio, modalidad)
VALUES 
('Curso completo de cocina asiática con técnicas tradicionales y modernas.',
 'Sushi, ramen, curry tailandés, técnicas de wok, ingredientes y especias asiáticas.',
 'Conocimientos básicos de cocina, utensilios de cocina básicos, ingredientes básicos asiáticos.',
 40, 23000.00, 'presencial'),

('Curso intensivo de pastelería saludable sin azúcares refinados.',
 'Tortas, budines, galletas con harinas integrales y endulzantes naturales.',
 'Equipamiento básico de repostería, horno eléctrico o a gas, ingredientes saludables.',
 30, 18000.00, 'presencial'),

('Curso avanzado de platos internacionales con técnicas de alta cocina.',
 'Cocina francesa, italiana, mexicana, montaje profesional, emplatados gourmet.',
 'Conocimientos intermedios de cocina, utensilios profesionales, ingredientes variados.',
 50, 20000.00, 'presencial'),
 ('Curso especializado en técnicas y cortes para parrilla argentina tradicional.',
 'Encendido de fuego, manejo de carbón y leña, cortes vacunos, marinados y achuras.',
 'Conocimientos básicos de cocina, parrilla o asador, utensilios para parrilla.',
 35, 25000.00, 'presencial'),
 ('Curso de Conservas Caseras',
 'Técnicas de estarilización, y como lograr hacer conservas tanto dulces como saladas.',
 'No hace falta conocimientos previos dado que es un curso de nivel básico.',
 50, 20000.00, 'presencial'),
 ('Curso de Cocina Regional Argentina',
 'Técnicas de estarilización, y como lograr hacer conservas tanto dulces como saladas.',
 'No hace falta conocimientos previos dado que es un curso de nivel básico.Para los elementos que se usaran, son diferentes cortes de carnes, especias, y tapas de empanadas. ',
 50, 20000.00, 'presencial'),
('Curso de Cocina para Niños','Recetas fáciles y seguras para niños: galletitas, pizzetas, muffins, ensaladas divertidas','Edad entre 8 y 13 años, autorización de un adulto', 10,8000.00,'presencial'),
('Curso de Cocina Vegetariana','Platos sin carne: hamburguesas vegetales, guisos con legumbres, ensaladas completas','Conocimientos básicos de cocina saludable',15,12000.00,'presencial');

INSERT INTO cronogramaCursos (idSede, idCurso, fechaInicio, fechaFin, vacantesDisponibles)
VALUES 
(1, 1, '2025-07-01', '2025-08-15', 12),  -- Palermo - Cocina Asiatica
(2, 2, '2025-07-10', '2025-08-20', 8),   -- Caballito - Pastelería Creativa
(3, 3, '2025-08-01', '2025-09-05', 10),  -- Belgrano - Platos Internacionales
(1, 4, '2025-09-10', '2025-10-25', 15);  -- Palermo - Parrilla

INSERT INTO asistenciaCursos (idAlumno, idCronograma, fecha)
VALUES 
(1, 1, '2025-07-02 18:30:00'),
(3, 1, '2025-07-02 18:30:00'),
(2, 2, '2025-07-11 10:00:00'),
(1, 2, '2025-07-11 10:00:00'),
(3, 3, '2025-08-02 09:30:00'), 
(6, 3, '2025-08-02 09:30:00'),
(4, 1, '2025-07-02 18:30:00'),
(6, 1, '2025-07-02 18:30:00'), 
(2, 4, '2025-09-11 17:00:00'),
(5, 4, '2025-09-11 17:00:00'); 

-- extras

INSERT INTO passwords (idpassword, password)
VALUES
(1,  'ana123'),
(2,  'lucasr'),
(3,  'marial'),
(4,  'jperez'),
(5,  'carlad'),
(6,  'msosa89'),
(7,  'sofi_fz'),
(8,  'diegom'),
(9,  'paulam'),
(10, 'fercast'),
(11, 'laurar'),
(12, 'dtorres'),
(13, 'carovaz'); 

INSERT INTO estadoReceta (idReceta, estado, fecha_creacion)
VALUES
(1, 'aprobado', '2025-05-15 14:23:00'),
(2, 'aprobado', '2025-05-20 09:45:00'),
(3, 'aprobado', '2025-06-01 16:30:00'),
(4, 'aprobado', '2025-06-10 11:15:00'),
(5, 'aprobado', '2025-05-15 14:23:00'),
(6, 'aprobado', '2025-05-20 09:45:00'),
(7, 'pendiente', '2025-06-01 16:30:00'),
(8, 'pendiente', '2025-06-10 11:15:00');

INSERT INTO multimedia (idPaso, tipo_contenido, extension, urlContenido)
VALUES 
(7, 'foto', '.jpg', 'recetaRisottoP0.jpg'),
(16, 'foto', '.jpg', 'recetaCheesecakeP0.jpg'),
(3, 'foto', '.jpg', 'recetaBerenjenaP3.jpg'),
(22, 'foto', '.jpg', 'recetaEmpanadasCarneP0.jpg'),
(5, 'foto', '.jpg', 'cousCousVegP2.jpg'),
(14, 'foto', '.jpg', 'mousseChocoP2.jpg');