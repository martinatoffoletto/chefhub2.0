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
('carolina.vazquez@email.com','carovaz',   'Si', 'Carolina Vázquez','Boulevard Oroño 45', 'img/cocinero1.png'),
('jorge.mendez@email.com', 'jorgem', 'Si', 'Jorge Méndez', 'Av. Corrientes 123', 'img/cocinero2.png'),
('valeria.suarez@email.com', 'valesu', 'Si', 'Valeria Suárez', 'Calle Libertad 456', 'img/cocinero3.png');


INSERT INTO alumnos (idAlumno, numeroTarjeta, dniFrente, dniFondo, tramite, cuentaCorriente) VALUES
(1, '123456789012', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000001', 0.50),
(2, '234567890123', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000002', 2450.00),
(3, '345678901234', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000003', 0.00), -- los casos donde esta en 0, es porque estan al dia con los pagos de los cursos
(4, '456789012345', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000004', 1800.00),
(5, '567890123456', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000005', 500.25),
(6, '678901234567', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000006', 0.00),
(7, '789012345678', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000007', 1750.80),
(8, '890123456789', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000008', 0.00),
(14, '901234567890', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000014', 0.00),
(15, '012345678901', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000015', 100.00);

INSERT INTO tiposReceta (descripcion) VALUES
('Postres y dulces'),
('Entrantes y aperitivos'),
('Platos principales'),
('Ensaladas'),
('Sopas y cremas'),
('Bebidas'),
('Salsas y aderezos'),
('Panadería y repostería'),
('Tapas y bocadillos'),
('Comida rápida');

INSERT INTO recetas (idUsuario, nombreReceta, descripcionReceta, fotoPrincipal, porciones, cantidadPersonas, idTipo) VALUES
(1, 'Lasaña vegetariana de berenjenas', 'Una receta nutritiva y sabrosa de lasaña sin carne, con capas de berenjena, ricotta y salsa de tomate casera.', 'img/rBerenjena.jpg', 8, 4, 3),
(1, 'Cous cous con vegetales', 'Una comida rápida, sabrosa y colorida con verduras salteadas.', 'img/cousCousveg.jpg', 4, 2, 4),
(2, 'Rissotto', 'Rissotto cremoso y reconfortante para clima frio.', 'img/rRisotto.jpg', 6, 3, 5),
(2, 'Pan casero', 'Pan artesanal con corteza crujiente y miga suave.', 'img/rPanArtesanal.jpg', 1, 10, 8),
(3, 'Mousse de chocolate', 'Postre ligero y esponjoso de chocolate amargo.', 'img/mousseChoco.jpg', 6, 6, 1),
(4, 'Cheescake de Frutilla', 'Tarta fría con base de galletitas y relleno de queso crema, cubierta con salsa de frutillas frescas.', 'img/rBerenjena.jpg', 1, 8, 1),
(4, 'Ensalada tibia de lentejas', 'Una ensalada nutritiva y reconfortante con lentejas, zanahoria, cebolla morada y un toque de limón.', 'img/rBerenjena.jpg', 2, 2, 4),
(3, 'Empanadas salteñas', 'Empanadas argentinas tradicionales con carne jugosa, cebolla, huevo y especias de Salta.', 'img/rEmpanadasCarne.jpg', 12, 6, 3),
(5, 'Tarta de Manzana', 'Tarta clásica con manzanas frescas y canela.', 'img/manzanaCanela.jpg', 8, 8, 1),
(6, 'Brownies de Chocolate', 'Brownies húmedos y chocolatosos.', 'img/rBrownies.jpg', 12, 12, 1),
(7, 'Budín de Banana', 'Budín húmedo de banana y nuez.', 'img/rBudinBanana.jpg', 10, 10, 1),
(8, 'Empanadas de Espinaca', 'Empanadas rellenas de espinaca y queso.', 'img/empanadasEspinaca.jpg', 12, 6, 3),
(9, 'Panqueques con Miel', 'Panqueques esponjosos con miel.', 'img/panquequesMiel.jpg', 8, 4, 1),
(14, 'Pizza Margarita', 'Pizza clásica con tomate, mozzarella y albahaca.', 'img/pizzaMargarita.jpeg', 8, 4, 9),
(15, 'Sandwich de Pollo', 'Sandwich rápido con pollo, tomate y lechuga.', 'img/sandwichPollo.jpg', 2, 2, 10);

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
('Arroz'),
('Manzana'), ('Canela'), ('Banana'), ('Nuez'), ('Espinaca'), ('Queso'), ('Miel'),
('Queso rallado'),
('Tomate'),
('Pollo'),
('Jamón'),
('Leche');

INSERT INTO unidades (descripcion) VALUES
('g'),
('kg'),
('ml'),
('l'),
('taza'),
('unidad'),
('rodaja');

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
(8, 6, 3, 5, 'Huevos para relleno y masa'), 
(9, 1, 3, 3, 'Manzanas verdes'),
(9, 2, 2, 1, 'Canela en polvo'),
(9, 3, 200, 1, 'Harina para la masa'),
(10, 8, 200, 1, 'Chocolate amargo'),
(10, 6, 3, 5, 'Huevos'),
(10, 4, 100, 1, 'Harina'),
(11, 3, 2, 3, 'Bananas maduras'),
(11, 4, 200, 1, 'Harina'),
(11, 9, 50, 1, 'Nuez picada'),
(12, 5, 300, 1, 'Espinaca cocida'),
(12, 6, 100, 1, 'Queso cremoso'),
(12, 4, 200, 1, 'Harina para la masa'),
(13, 4, 150, 1, 'Harina'),
(13, 6, 2, 5, 'Huevos'),
(13, 7, 50, 1, 'Miel'),
(14, 25, 200, 1, 'Queso rallado para la pizza'),
(14, 26, 2, 12, 'Rodajas de tomate'),
(14, 3, 300, 1, 'Harina para la masa'),
(15, 27, 1, 13, 'Pechuga de pollo cocida'),
(15, 28, 2, 12, 'Rodajas de jamón'),
(15, 26, 2, 12, 'Rodajas de tomate');

INSERT INTO calificaciones (idusuario, idReceta, calificacion, comentarios) VALUES -- consideramos puntuacion del 1 al 5
(1, 1, 5, 'Excelente receta, muy bien explicada y deliciosa.'),
(2, 3, 4, 'Muy buena sopa, perfecta para el invierno.'),
(3, 5, 3, 'El mousse quedó un poco dulce para mi gusto, pero rico.'),
(5, 5, 5, 'El mousse quedó muy rico.'),
(7, 1, 5, 'Receta fácil y rápida, muy buena.'),
(2, 3, 5, 'Muy rica sopa !!'),
(2, 9, 5, 'Muy rica la tarta de manzana!'),
(3, 10, 4, 'Brownies bien húmedos.'),
(4, 11, 5, 'El budín de banana esponjoso.'),
(5, 12, 4, 'Empanadas sabrosas.'),
(6, 13, 5, 'Panqueques fáciles y ricos.'),
(14, 14, 5, 'La pizza salió espectacular.'),
(15, 15, 4, 'Sandwich rápido y rico.');

INSERT INTO estadoComentario (idCalificacion, estado, fechaEstado, observaciones) VALUES
(1,  'aprobado',  GETDATE(), ''),
(2,  'aprobado',  GETDATE(), ''),
(3,  'aprobado',  GETDATE(), ''),
(4,  'pendiente',  GETDATE(), ''),
(5,  'aprobado',  GETDATE(), ''),
(6,  'aprobado',  GETDATE(), ''),
(7,  'aprobado',  GETDATE(), ''),
(8,  'aprobado',  GETDATE(), ''),
(9,  'aprobado',  GETDATE(), ''),
(10, 'aprobado',  GETDATE(), ''),
(11, 'aprobado',  GETDATE(), ''),
(12, 'aprobado',  GETDATE(), ''),
(13, 'aprobado',  GETDATE(), '');
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
(8, 3, 'Hornear hasta que estén doradas y crujientes.'),
(9, 1, 'Preparar la masa con harina y manteca.'),
(9, 2, 'Cortar las manzanas y mezclar con canela.'),
(9, 3, 'Armar la tarta y hornear.'),
(10, 1, 'Derretir el chocolate y mezclar con huevos.'),
(10, 2, 'Agregar harina y mezclar.'),
(10, 3, 'Hornear hasta que estén húmedos.'),
(11, 1, 'Pisar las bananas y mezclar con harina.'),
(11, 2, 'Agregar nuez y mezclar.'),
(11, 3, 'Hornear hasta dorar.'),
(12, 1, 'Saltear la espinaca y mezclar con queso.'),
(12, 2, 'Rellenar las tapas y cerrar.'),
(12, 3, 'Hornear hasta dorar.'),
(13, 1, 'Mezclar harina y huevos.'),
(13, 2, 'Cocinar los panqueques en sartén.'),
(13, 3, 'Servir con miel.'),
(14, 1, 'Preparar la masa de pizza y dejar levar.'),
(14, 2, 'Agregar salsa de tomate, queso rallado y rodajas de tomate.'),
(14, 3, 'Hornear hasta que el queso se derrita.'),
(15, 1, 'Cocinar la pechuga de pollo y cortar en tiras.'),
(15, 2, 'Armar el sandwich con pollo, jamón y tomate.'),
(15, 3, 'Servir frío o caliente.');

INSERT INTO fotos (idReceta, urlFoto, extension) VALUES
(1, 'img/rBerenjena.jpg', '.jpg'),
(2, 'img/cousCousveg.jpg', '.jpg'),
(3, 'img/rRisotto.jpg', '.jpg'),
(4, 'img/rPanArtesanal.jpg', '.jpg'),
(5, 'img/mousseChoco.jpg', '.jpg'),
(6, 'img/rCheesecake.jpg', '.jpg'),
(7, 'img/rLentejas.jpg', '.jpg'),
(8, 'img/rEmpanadasCarne.jpg', '.jpg'),
(9, 'img/manzanaCanela.jpg', '.jpg'),
(10, 'img/rBrownies.jpg', '.jpg'),
(11, 'img/rBudinBanana.jpg', '.jpg'),
(12, 'img/empanadasEspinaca.jpg', '.jpg'),
(13, 'img/panquequesMiel.jpg', '.jpg'),
(14, 'img/pizzaMargarita.jpeg', '.jpeg'),
(15, 'img/sandwichPollo.jpg', '.jpg');

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
),
(
    'Sede Centro',
    'Av. 9 de Julio 1000, CABA',
    '01140001234',
    'centro@cocinaedu.ar',
    '5491198765432',
    'Descuento del 5%',
    5.00,
    'Descuento del 10%',
    10.00
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
('Curso de Cocina Vegetariana','Platos sin carne: hamburguesas vegetales, guisos con legumbres, ensaladas completas','Conocimientos básicos de cocina saludable',15,12000.00,'presencial'),
('Curso de Pizzas Artesanales', 'Masa, salsa, toppings, horneado.', 'Ninguno.', 20, 15000.00, 'presencial');

INSERT INTO cronogramaCursos (idSede, idCurso, fechaInicio, fechaFin, vacantesDisponibles)
VALUES 
(1, 1, '2025-07-01', '2025-08-15', 12),  -- Palermo - Cocina Asiatica
(2, 2, '2025-07-10', '2025-08-20', 8),   -- Caballito - Pastelería Creativa
(3, 3, '2025-08-01', '2025-09-05', 10),  -- Belgrano - Platos Internacionales
(1, 4, '2025-09-10', '2025-10-25', 15),  -- Palermo - Parrilla
(4, 9, '2025-10-01', '2025-11-01', 20);  -- Centro - Pizzas Artesanales

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
(5, 4, '2025-09-11 17:00:00'),
(14, 5, '2025-10-02 18:00:00'),
(15, 5, '2025-10-02 18:00:00'); 

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
(13, 'carovaz'),
(14, 'jorgem'),
(15, 'valesu'); 

INSERT INTO estadoReceta (idReceta, estado, fecha_creacion)
VALUES
(1, 'aprobado', '2025-05-15 14:23:00'),
(2, 'aprobado', '2025-05-20 09:45:00'),
(3, 'aprobado', '2025-06-01 16:30:00'),
(4, 'aprobado', '2025-06-10 11:15:00'),
(5, 'aprobado', '2025-05-15 14:23:00'),
(6, 'aprobado', '2025-05-20 09:45:00'),
(7, 'pendiente', '2025-06-01 16:30:00'),
(8, 'pendiente', '2025-06-10 11:15:00'),
(9, 'aprobado', '2025-06-15 10:00:00'),
(10, 'aprobado', '2025-06-16 11:00:00'),
(11, 'pendiente', '2025-06-17 12:00:00'),
(12, 'pendiente', '2025-06-18 13:00:00'),
(13, 'aprobado', '2025-06-19 14:00:00'),
(14, 'aprobado', '2025-06-20 10:00:00'),
(15, 'pendiente', '2025-06-21 11:00:00');

INSERT INTO multimedia (idPaso, tipo_contenido, extension, urlContenido)
VALUES 
(7, 'foto', '.jpg', 'recetaRisottoP0.jpg'),
(16, 'foto', '.jpg', 'recetaCheesecakeP0.jpg'),
(3, 'foto', '.jpg', 'recetaBerenjenaP3.jpg'),
(22, 'foto', '.jpg', 'recetaEmpanadasCarneP0.jpg'),
(5, 'foto', '.jpg', 'cousCousVegP2.jpg'),
(14, 'foto', '.jpg', 'mousseChocoP2.jpg'),
(37, 'foto', '.jpg', 'pizzaMargaritaP1.jpg'),
(40, 'foto', '.jpg', 'sandwichPolloP1.jpg');


INSERT INTO recetasFavoritas (idCreador, idReceta) VALUES
(1, 9),   -- Ana Gómez favorita Tarta de Manzana
(2, 10),  -- Lucas Rojas favorita Brownies de Chocolate
(3, 11),  -- María López favorita Budín de Banana
(4, 14),  -- Juan Pérez favorita Pizza Margarita
(5, 15),  -- Carla Díaz favorita Sandwich de Pollo
(14, 1),  -- Jorge Méndez favorita Lasaña vegetariana de berenjenas
(15, 2);  -- Valeria Suárez favorita Cous cous con vegetales

-- Puedes agregar más relaciones según tus usuarios y recetas existentes.