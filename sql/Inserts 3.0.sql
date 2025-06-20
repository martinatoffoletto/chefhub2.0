﻿use chefhub; 

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
('valeria.suarez@email.com', 'valesu', 'Si', 'Valeria Suárez', 'Calle Libertad 456', 'img/cocinero2.png'),
('fernando.sosa@email.com',    'fsosa89',    'Si', 'Fernando Sosa',     'Calle 911 de Julio 234', 'img/cocinero1.png'),
('sofia.sosa@email.com','sofi_fz',    'Si', 'Sofía Sosa', 'Diagonal Norte 3241', 'img/cocinero1.png'),
('diego.Sosa@email.com', 'diegos',     'Si', 'Diego Sosa',  'Boulevard Mitre 142', 'img/cocinero1.png'),
('paulaAli@email.com',    'paulaaa',    'Si', 'Paula Ali',    'Av. Córdoba 124', 'img/cocinero1.png'),
('fernando.Ali@email.com', 'ferali',   'Si', 'Fernando Ali', 'Calle Belgrano 5647', 'img/cocinero1.png'),
('laura.Ali@email.com',     'lauraali',    'Si', 'Laura Ali',     'Paseo Colon 8490', 'img/cocinero1.png'),
('diego.Ali@email.com',    'dAli',   'Si', 'Diego Ali',    'Av. San Martin 2434', 'img/cocinero1.png'),
('carolina.Ali@email.com','caroAli',   'Si', 'Carolina Ali','Boulevard Oroño 445', 'img/cocinero1.png'),
('jorge.Ali@email.com', 'jorgemAli', 'Si', 'Jorge Ali', 'Av. Corrientes 1243', 'img/cocinero2.png'),
('valeria.Ali@email.com', 'valeAli', 'Si', 'Valeria Ali', 'Calle Libertad 4456', 'img/cocinero2.png');


INSERT INTO alumnos (idAlumno, numeroTarjeta, dniFrente, dniFondo, tramite, cuentaCorriente) VALUES
(1, '123456789012', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000001', 0.50),
(2, '234567890123', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000002', 2450.00),
(3, '345678901234', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000003', 0.00), -- los casos donde esta en 0, es porque estan al dia con los pagos de los cursos
(4, '456789012345', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000004', 1800.00),
(5, '567890123456', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000005', 500.25),
(6, '678901234567', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000006', 0.00),
(7, '789012345678', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000007', 1750.80),
(8, '890123456789', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000008', 0.10),
(9, '890123456781', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000009', 0.20),
(10, '890123456782', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000099', 0.30),
(11, '890123456783', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000088', 0.40),
(12, '890123456784', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000077', 0.50),
(13, '890123456785', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000066', 0.60),
(14, '901234567890', 'img/dniFrente.jpg', 'img/dniDorso.jpg', '10000000014', 0.220),
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
(3, 'Cheescake de Frutilla', 'Tarta fría con base de galletitas y relleno de queso crema, cubierta con salsa de frutillas frescas.', 'img/rCheesecake.jpg', 1, 8, 1),
(4, 'Ensalada tibia de lentejas', 'Una ensalada nutritiva y reconfortante con lentejas, zanahoria, cebolla morada y un toque de limón.', 'img/rLentejas.jpg', 2, 2, 4),
(4, 'Empanadas salteñas', 'Empanadas argentinas tradicionales con carne jugosa, cebolla, huevo y especias de Salta.', 'img/rEmpanadasCarne.jpg', 12, 6, 3),
(5, 'Tarta de Manzana', 'Tarta clásica con manzanas frescas y canela.', 'img/manzanaCanela.jpg', 8, 8, 1),
(5, 'Brownies de Chocolate', 'Brownies húmedos y chocolatosos.', 'img/rBrownies.jpg', 12, 12, 1),
(5, 'Budín de Banana', 'Budín húmedo de banana y nuez.', 'img/rBudinBanana.jpg', 10, 10, 1),
(6, 'Empanadas de Espinaca', 'Empanadas rellenas de espinaca y queso.', 'img/empanadasEspinaca.jpg', 12, 6, 3),
(7, 'Panqueques con Miel', 'Panqueques esponjosos con miel.', 'img/panquequesMiel.jpg', 8, 4, 1),
(8, 'Pizza Margarita', 'Pizza clásica con tomate, mozzarella y albahaca.', 'img/pizzaMargarita.jpeg', 8, 4, 9),
(9, 'Sandwich de Pollo', 'Sandwich rápido con pollo, tomate y lechuga.', 'img/sandwichPollo.jpg', 2, 2, 10),
(10, 'Bruschettas de tomate y albahaca', 'Entrante italiano clásico con pan tostado, tomate fresco, ajo y albahaca.', 'img/bruschettas.jpg', 6, 3, 2),
(11, 'Tacos de pescado', 'Tortillas rellenas con pescado rebozado, repollo y salsa cremosa.', 'img/tacosPescado.jpg', 8, 4, 9),
(12, 'Helado casero de frutilla', 'Postre refrescante hecho con frutillas frescas, crema y un toque de limón.', 'img/heladoFrutilla.jpg', 6, 6, 1),
(13, 'Quiche de puerros', 'Tarta salada con masa quebrada, puerros salteados y crema de huevo.', 'img/quichePuerros.jpg', 8, 4, 3),
(14, 'Hamburguesas de garbanzos', 'Hamburguesas vegetarianas ricas en proteínas, acompañadas con pan casero y vegetales.', 'img/hamburguesasGarbanzos.jpg', 4, 2, 10),
(15, 'Sopa crema de calabaza', 'Sopa suave y reconfortante con calabaza, crema y un toque de nuez moscada.', 'img/sopaCalabaza.jpg', 4, 4, 5),
(15, 'Tarta de coco y dulce de leche', 'Tarta dulce con base crocante, dulce de leche y cobertura de coco rallado.', 'img/tartaCocoDDL.jpg', 8, 8, 8),
(15, 'Albóndigas con salsa de tomate', 'Albóndigas caseras de carne servidas con una sabrosa salsa de tomate.', 'img/albondigasSalsa.jpg', 6, 3, 3),
(15, 'Ñoquis de papa', 'Ñoquis suaves caseros acompañados con salsa bolognesa o pesto.', 'img/ñoquisPapa.jpg', 6, 3, 3),
(15, 'Arroz con leche', 'Postre tradicional a base de arroz, leche, azúcar y canela.', 'img/arrozConLeche.jpg', 6, 6, 1);

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
('Manzana'), 
('Canela'), 
('Banana'), 
('Nuez'), 
('Espinaca'), 
('Queso'), 
('Miel'),
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
(1, 11, 500, 7, 'Rodajas para capas'),
(1, 12, 300, 1, 'Ricota para relleno'),
(1, 13, 400, 3, 'Salsa de tomate casera'),
(2, 1, 200, 1, 'Cous cous cocido'),
(2, 7, 300, 1, 'Vegetales variados'),
(2, 4, 30, 3, 'Aceite de oliva para saltear'),
(3, 5, 150, 1, 'Cebolla picada'),
(3, 6, 3, 6, 'Huevos para acompañar'),
(3, 4, 20, 3, 'Aceite de oliva para sofreír'),
(4, 3, 500, 1, 'Harina para la masa'),
(4, 10, 15, 1, 'Levadura fresca'),
(4, 4, 25, 3, 'Aceite de oliva'),
(5, 8, 200, 1, 'Chocolate amargo'),
(5, 6, 3, 6, 'Huevos para la mousse'),
(5, 9, 150, 1, 'Frutillas frescas para decoración'),
(6, 3, 200, 1, 'Harina para base'),
(6, 12, 400, 1, 'Queso crema para relleno'),
(6, 9, 150, 1, 'Frutillas frescas para cobertura'),
(7, 17, 300, 1, 'Lentejas cocidas '),
(7, 5, 100, 1, 'Cebolla morada picada'),
(7, 14, 50, 1, 'Morron picado'),
(8, 2, 400, 1, 'Carne picada'),
(8, 5, 150, 1, 'Cebolla picada'),
(8, 6, 3, 6, 'Huevos para relleno y masa'), 
(9, 19, 3, 6, 'Manzanas verdes'),
(9, 20, 2, 1, 'Canela en polvo'),
(9, 3, 200, 1, 'Harina para la masa'),
(10, 8, 200, 1, 'Chocolate amargo'),
(10, 6, 3, 6, 'Huevos'),
(10, 3, 100, 1, 'Harina'),
(11, 21, 2, 1, 'Bananas maduras'),
(11, 3, 200, 1, 'Harina'),
(11, 22, 50, 1, 'Nuez picada'),
(12, 7, 300, 1, 'Espinaca cocida'),
(12, 24, 100, 1, 'Queso cremoso'),
(12, 3, 200, 1, 'Harina para la masa'),
(13, 3, 150, 1, 'Harina'),
(13, 6, 2, 6, 'Huevos'),
(13, 25, 50, 3, 'Miel'),
(14, 26, 200, 1, 'Queso rallado para la pizza'),
(14, 26, 2, 7, 'Rodajas de tomate'),
(14, 3, 300, 1, 'Harina para la masa'),
(15, 28, 1, 1, 'Pechuga de pollo cocida'),
(15, 29, 2, 7, 'Rodajas de jamón'),
(15, 27, 2, 7, 'Rodajas de tomate'),
(16, 17, 300, 1, 'Lentejas cocidas'),
(16, 5, 100, 1, 'Cebolla picada'),
(16, 14, 50, 1, 'Morrón picado'),
(16, 2, 200, 1, 'Carne picada'),
(17, 3, 100, 1, 'Harina para rebozar'),
(17, 4, 20, 3, 'Aceite de oliva para freír'),
(17, 13, 2, 6, 'Tomate'),
(17, 5, 50, 1, 'Cebolla en juliana'),
(18, 9, 300, 1, 'Frutillas frescas'),
(18, 30, 200, 3, 'Leche entera'),
(18, 6, 3, 6, 'Huevos'),
(19, 5, 150, 1, 'Cebolla'),
(19, 6, 3, 6, 'Huevos'),
(19, 30, 100, 3, 'Leche'),
(19, 3, 200, 1, 'Harina para base'),
(20, 7, 300, 1, 'Vegetales cocidos'),
(20, 6, 2, 6, 'Huevos'),
(20, 3, 100, 1, 'Harina para unir'),
(21, 5, 100, 1, 'Cebolla salteada'),
(21, 30, 200, 3, 'Leche para cremosidad'),
(21, 4, 10, 3, 'Aceite de oliva'),
(22, 9, 100, 1, 'Frutillas decorativas'),
(22, 30, 200, 3, 'Leche condensada'),
(22, 3, 250, 1, 'Harina para masa'),
(23, 2, 300, 1, 'Carne picada'),
(23, 5, 100, 1, 'Cebolla picada'),
(23, 13, 200, 3, 'Salsa de tomate casera'),
(24, 3, 300, 1, 'Harina'),
(24, 6, 1, 6, 'Huevo'),
(24, 26, 100, 1, 'Queso rallado para servir'),
(25, 18, 200, 1, 'Arroz blanco'),
(25, 30, 500, 3, 'Leche entera'),
(25, 20, 1, 5, 'Canela en rama');

INSERT INTO calificaciones (idusuario, idReceta, calificacion, comentarios) VALUES -- consideramos puntuacion del 1 al 5
(2, 1, 5, 'Excelente receta, muy bien explicada y deliciosa.'),
(2, 2, 4, 'Muy sabrosa receta.'),
(3, 3, 4, 'Muy detallada y facil de seguir.'),
(3, 4, 4, 'Muy sabrosa receta.'),
(1, 5, 3, 'El mousse quedó un poco dulce para mi gusto, pero rico.'),
(11, 5, 5, 'El mousse quedó muy rico.'),
(1, 6, 5, 'Receta fácil y rápida, muy buena.'),
(1, 7, 5, 'Muy rica sopa !!'),
(1, 9, 5, 'Muy rica la tarta de manzana!'),
(1, 10, 4, 'Brownies bien húmedos.'),
(2, 11, 5, 'El budín de banana esponjoso.'),
(2, 12, 4, 'Empanadas sabrosas.'),
(2, 13, 5, 'Panqueques fáciles y ricos.'),
(2, 14, 5, 'La pizza salió espectacular.'),
(3, 15, 4, 'Excelente receta, muy bien explicada y deliciosa.'),
(3, 16, 4, 'Excelente receta, muy bien explicada y deliciosa.'),
(7, 17, 4, 'Excelente receta, muy bien explicada y deliciosa.'),
(3, 18, 5, 'Excelente receta, muy bien explicada y deliciosa.'),
(4, 19, 5, 'Excelente receta, muy bien explicada y deliciosa.'),
(4, 20, 5, 'Receta que llena y es deliciosa.'),
(4, 21, 5, 'Receta fácil y rápida, muy buena.'),
(4, 23, 5, 'Muy rica receta !!'),
(4, 22, 5, 'Muy rica la tarta de manzana!'),
(5, 1, 4, 'Muy buena receta.'),
(5, 2, 1, 'Receta complicada de seguir.'),
(5, 6, 5, 'Excelente receta, muy bien explicada y deliciosa.'),
(5, 7, 5, 'Excelente receta, muy bien explicada y deliciosa.'),
(10, 8, 4, 'Excelente receta, muy bien explicada y deliciosa.'),
(5, 8, 1, 'Receta complicada de seguir.');

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
(13, 'aprobado',  GETDATE(), ''),
(14,  'pendiente',  GETDATE(), ''),
(15,  'aprobado',  GETDATE(), ''),
(16, 'aprobado',  GETDATE(), ''),
(17, 'aprobado',  GETDATE(), ''),
(18, 'aprobado',  GETDATE(), ''),
(19, 'aprobado',  GETDATE(), ''),
(20,'aprobado',  GETDATE(), ''),
(21, 'aprobado',  GETDATE(), ''),
(22, 'aprobado',  GETDATE(), ''),
(23, 'aprobado',  GETDATE(), ''),
(24,  'pendiente',  GETDATE(), ''),
(25,  'aprobado',  GETDATE(), ''),
(26,  'aprobado',  GETDATE(), ''),
(27,  'aprobado',  GETDATE(), ''),
(28,  'aprobado',  GETDATE(), ''),
(29,  'pendiente',  GETDATE(), '');
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
(15, 3, 'Servir frío o caliente.'),
(16, 1, 'Cortar el pan en rodajas y tostar ligeramente.'),
(16, 2, 'Frotar con ajo para dar sabor.'),
(16, 3, 'Agregar rodajas de tomate y mozzarella.'),
(16, 4, 'Decorar con hojas de albahaca y un chorrito de aceite de oliva.'),
(17, 1, 'Cortar el pescado en tiras y condimentar.'),
(17, 2, 'Rebozar el pescado y freírlo hasta que esté dorado.'),
(17, 3, 'Calentar las tortillas.'),
(17, 4, 'Armar los tacos con pescado, repollo y salsa cremosa.'),
(18, 1, 'Lavar y triturar las frutillas.'),
(18, 2, 'Mezclar con crema y jugo de limón.'),
(18, 3, 'Llevar al congelador removiendo cada 30 minutos.'),
(19, 1, 'Preparar la masa y forrar el molde.'),
(19, 2, 'Saltear los puerros en manteca.'),
(19, 3, 'Batir los huevos con crema y mezclar con los puerros.'),
(19, 4, 'Verter la mezcla sobre la masa y hornear.'),
(20, 1, 'Procesar los garbanzos cocidos con condimentos.'),
(20, 2, 'Formar las hamburguesas.'),
(20, 3, 'Cocinar en sartén o al horno.'),
(20, 4, 'Servir con pan y vegetales.'),
(21, 1, 'Cortar y hervir la calabaza hasta que esté tierna.'),
(21, 2, 'Procesar con caldo y crema.'),
(21, 3, 'Agregar nuez moscada y rectificar sal.'),
(21, 4, 'Calentar y servir.'),
(22, 1, 'Preparar una base de masa y hornear.'),
(22, 2, 'Cubrir con dulce de leche.'),
(22, 3, 'Espolvorear con coco rallado y gratinar levemente.'),
(23, 1, 'Mezclar carne con condimentos y formar albóndigas.'),
(23, 2, 'Dorar las albóndigas en una sartén.'),
(23, 3, 'Cocinar en salsa de tomate durante 20 minutos.'),
(24, 1, 'Hervir las papas y hacer un puré.'),
(24, 2, 'Agregar harina y formar una masa suave.'),
(24, 3, 'Formar cilindros, cortar y marcar con tenedor.'),
(24, 4, 'Hervir hasta que floten y servir con salsa.'),
(25, 1, 'Hervir el arroz en agua durante 5 minutos y escurrir.'),
(25, 2, 'Colocar el arroz con leche, azúcar y cáscara de limón en una olla.'),
(25, 3, 'Cocinar a fuego lento, revolviendo constantemente, hasta que espese.'),
(25, 4, 'Retirar la cáscara y servir frío o tibio con canela espolvoreada.');

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
(15, 'img/sandwichPollo.jpg', '.jpg'),
(16, 'img/bruschettas.jpg', '.jpg'),
(17, 'img/tacosPescado.jpg', '.jpg'),
(18, 'img/heladoFrutilla.jpg', '.jpg'),
(19, 'img/quichePuerros.jpg', '.jpg'),
(20, 'img/hamburguesasGarbanzos.jpg', '.jpg'),
(21, 'img/sopaCalabaza.jpg', '.jpg'),
(22, 'img/tartaCocoDDL.jpg', '.jpg'),
(23, 'img/albondigasSalsa.jpg', '.jpg'),
(24, 'img/ñoquisPapa.jpg', '.jpg'),
(25, 'img/arrozConLeche.jpg', '.jpg');

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
('Curso completo de cocina asiática con técnicas tradicionales y modernas.', 'Sushi, ramen, curry tailandés, técnicas de wok, ingredientes y especias asiáticas.', 'Conocimientos básicos de cocina, utensilios de cocina básicos, ingredientes básicos asiáticos.', 40, 23000.00, 'presencial'),
('Curso intensivo de pastelería saludable sin azúcares refinados.', 'Tortas, budines, galletas con harinas integrales y endulzantes naturales.', 'Equipamiento básico de repostería, horno eléctrico o a gas, ingredientes saludables.', 30, 18000.00, 'presencial'),
('Curso avanzado de platos internacionales con técnicas de alta cocina.', 'Cocina francesa, italiana, mexicana, montaje profesional, emplatados gourmet.', 'Conocimientos intermedios de cocina, utensilios profesionales, ingredientes variados.', 50, 20000.00, 'presencial'),
('Curso especializado en técnicas y cortes para parrilla argentina tradicional.', 'Encendido de fuego, manejo de carbón y leña, cortes vacunos, marinados y achuras.','Conocimientos básicos de cocina, parrilla o asador, utensilios para parrilla.', 35, 25000.00, 'presencial'),
('Curso de Conservas Caseras', 'Técnicas de estarilización, y como lograr hacer conservas tanto dulces como saladas.', 'No hace falta conocimientos previos dado que es un curso de nivel básico.', 50, 20000.00, 'presencial'),
('Curso de Cocina Regional Argentina', 'Técnicas de estarilización, y como lograr hacer conservas tanto dulces como saladas.','No hace falta conocimientos previos dado que es un curso de nivel básico.Para los elementos que se usaran, son diferentes cortes de carnes, especias, y tapas de empanadas. ', 50, 20000.00, 'presencial'),
('Cocina Sin Gluten: Recetas para Celíacos', 'Sustitutos de harina, platos dulces y salados, precauciones de contaminación cruzada', 'Interés en cocinar sin gluten, utensilios limpios', 34, 9800.00, 'presencial'),
('Curso de Cocina para Niños','Recetas fáciles y seguras para niños: galletitas, pizzetas, muffins, ensaladas divertidas','Edad entre 8 y 13 años, autorización de un adulto', 30,8000.00,'presencial'),
('Curso de Cocina Vegetariana','Platos sin carne: hamburguesas vegetales, guisos con legumbres, ensaladas completas','Conocimientos básicos de cocina saludable',35,12000.00,'presencial'),
('Repostería Creativa sin Horno', 'Postres fríos, técnicas de gelificación, bases con galletas, decoración básica', 'Heladera y utensilios de cocina comunes', 30, 7500.00, 'virtual'),
('El Arte de las Pastas Caseras', 'Masa de pasta, rellenos, salsas clásicas, técnicas italianas tradicionales', 'Rodillo o máquina de pastas, ingredientes básicos',  32,  11000.00, 'presencial'),
('Curso de Pizzas Artesanales', 'Masa, salsa, toppings, horneado.', 'Ninguno.', 40, 15000.00, 'presencial');

INSERT INTO cronogramaCursos (idSede, idCurso, fechaInicio, fechaFin, vacantesDisponibles)
VALUES 
(1, 1, '2025-07-01', '2025-08-15', 12),  -- Palermo - Cocina Asiatica
(2, 2, '2025-07-10', '2025-08-20', 8),   -- Caballito - Pastelería Creativa
(3, 3, '2025-08-01', '2025-09-05', 10),  -- Belgrano - Platos Internacionales
(4, 4, '2025-09-10', '2025-10-25', 15),  -- Palermo - Parrilla
(2, 5, '2025-10-01', '2025-11-01', 20),
(4, 6, '2025-10-01', '2025-11-01', 20),
(4, 7, '2025-10-01', '2025-11-01', 20),
(3, 8, '2025-10-01', '2025-11-01', 20),
(3, 9, '2025-10-01', '2025-11-01', 20),
(1, 10, '2025-07-01', '2025-08-15', 12),  
(2, 11, '2025-07-10', '2025-08-20', 8),
(1, 12, '2025-07-01', '2025-08-15', 12),
(3, 11, '2025-07-10', '2025-08-20', 8),
(4, 12, '2025-07-01', '2025-08-15', 12);  

INSERT INTO asistenciaCursos (idAlumno, idCronograma, fecha)
VALUES 
(1, 1, '2025-07-02 18:30:00'),
(2, 1, '2025-07-02 18:30:00'),
(3, 2, '2025-07-11 10:00:00'),
(4, 2, '2025-07-11 10:00:00'),
(1, 3, '2025-08-02 09:30:00'), 
(2, 3, '2025-08-02 09:30:00'),
(3, 4, '2025-09-02 18:30:00'),
(4, 4, '2025-09-02 18:30:00'), 
(1, 5, '2025-10-11 17:00:00'),
(2, 5, '2025-10-11 17:00:00'),
(3, 6, '2025-10-02 18:00:00'),
(4, 6, '2025-10-02 18:00:00'),
(1, 7, '2025-07-02 18:30:00'),
(2, 7, '2025-07-02 18:30:00'),
(3, 8, '2025-07-11 10:00:00'),
(4, 8, '2025-07-11 10:00:00'),
(1, 9, '2025-08-02 09:30:00'), 
(2, 9, '2025-08-02 09:30:00'),
(3, 10, '2025-07-02 18:30:00'),
(4, 10, '2025-07-02 18:30:00'), 
(1, 11, '2025-07-11 17:00:00'),
(2, 12, '2025-07-11 17:00:00'),
(3, 11, '2025-07-11 18:00:00'),
(4, 12, '2025-07-02 18:00:00'); 

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
(15, 'valesu'),
(16,  'msosa89'),
(17,  'sofi_fz'),
(18,  'diegom'),
(19,  'paulam'),
(20, 'fercast'),
(21, 'laurar'),
(22, 'dtorres'),
(23, 'carovaz'),
(24, 'jorgem'),
(25, 'valesu'); 

INSERT INTO estadoReceta (idReceta, estado, fecha_creacion)
VALUES
(1, 'aprobado', '2025-05-15 14:23:00'),
(2, 'aprobado', '2025-05-20 09:45:00'),
(3, 'aprobado', '2025-06-01 16:30:00'),
(4, 'aprobado', '2025-06-10 11:15:00'),
(5, 'aprobado', '2025-05-15 14:23:00'),
(6, 'aprobado', '2025-05-20 09:45:00'),
(7, 'aprobado', '2025-06-01 16:30:00'),
(8, 'aprobado', '2025-06-10 11:15:00'),
(9, 'aprobado', '2025-06-15 10:00:00'),
(10, 'aprobado', '2025-06-16 11:00:00'),
(11, 'aprobado', '2025-06-17 12:00:00'),
(12, 'aprobado', '2025-06-18 13:00:00'),
(13, 'aprobado', '2025-05-15 14:23:00'),
(14, 'aprobado', '2025-05-20 09:45:00'),
(15, 'aprobado', '2025-06-01 16:30:00'),
(16, 'aprobado', '2025-06-10 11:15:00'),
(17, 'aprobado', '2025-06-15 10:00:00'),
(18, 'aprobado', '2025-06-16 11:00:00'),
(19, 'aprobado', '2025-06-17 12:00:00'),
(20, 'aprobado', '2025-06-18 13:00:00'),
(21, 'aprobado', '2025-05-15 14:23:00'),
(22, 'aprobado', '2025-05-20 09:45:00'),
(23, 'aprobado', '2025-06-01 16:30:00'),
(24, 'pendiente', '2025-06-10 11:15:00'),
(25, 'pendiente', '2025-05-15 14:23:00');

INSERT INTO multimedia (idPaso, tipo_contenido, extension, urlContenido)
VALUES 
(8, 'foto', '.jpg', 'recetaRisottoP0.jpg'),
(17, 'foto', '.jpg', 'recetaCheesecakeP0.jpg'),
(2, 'foto', '.jpg', 'recetaBerenjenaP3.jpg'),
(23, 'foto', '.jpg', 'recetaEmpanadasCarneP0.jpg'),
(5, 'foto', '.jpg', 'cousCousVegP2.jpg'),
(14, 'foto', '.jpg', 'mousseChocoP2.jpg'),
(1, 'video', '.mp4', 'lasagnaBerenjenas.mp4'),
(4, 'video', '.mp4', 'vcous.mp4'),
(7, 'video', '.mp4', 'risotto.mp4'),
(10, 'video', '.mp4', 'vpan.mp4'),
(13, 'video', '.mp4', 'mousseChocolate.mp4'),
(16, 'video', '.mp4', 'cheescake.mp4'),
(19, 'video', '.mp4', 'lentejasEnsalada.mp4'),
(22, 'video', '.mp4', 'empanadasCarne.mp4'),
(25, 'video', '.mp4', 'vman.mp4'),
(28, 'video', '.mp4', 'vbrownie.mp4'),
(31, 'video', '.mp4', 'vbudin.mp4'),
(34, 'video', '.mp4', 'vespinaca.mp4'),
(37, 'video', '.mp4', 'vpanqueque.mp4'),
(40, 'video', '.mp4', 'vmargarita.mp4'),
(43, 'video', '.mp4', 'vsanguche.mp4'),
(46, 'video', '.mp4', 'vBruschettas.mp4'),
(50, 'video', '.mp4', 'vtacos.mp4'),
(54, 'video', '.mp4', 'vhelado.mp4'),
(57, 'video', '.mp4', 'vquiche.mp4'),
(61, 'video', '.mp4', 'vhambur.mp4'),
(65, 'video', '.mp4', 'vsopa.mp4'),
(69, 'video', '.mp4', 'vtarta.mp4'),
(73, 'video', '.mp4', 'valbon.mp4'),
(76, 'video', '.mp4', 'vñoquis.mp4'),
(79, 'video', '.mp4', 'varroz.mp4');


INSERT INTO recetasFavoritas (idCreador, idReceta) VALUES
(1, 9),   -- Ana Gómez favorita Tarta de Manzana
(2, 10),  -- Lucas Rojas favorita Brownies de Chocolate
(3, 11),  -- María López favorita Budín de Banana
(4, 14),  -- Juan Pérez favorita Pizza Margarita
(5, 15),  -- Carla Díaz favorita Sandwich de Pollo
(6, 1),  -- Jorge Méndez favorita Lasaña vegetariana de berenjenas
(7, 11),  -- María López favorita Budín de Banana
(8, 14),  -- Juan Pérez favorita Pizza Margarita
(9, 15),  -- Carla Díaz favorita Sandwich de Pollo
(10, 11),  -- María López favorita Budín de Banana
(11, 14),  -- Juan Pérez favorita Pizza Margarita
(12, 15),  -- Carla Díaz favorita Sandwich de Pollo
(13, 2),
(14, 2),
(15, 2);  -- Valeria Suárez favorita Cous cous con vegetales

INSERT INTO notificaciones (descripcion, idUsuario) VALUES
-- Ana Gómez (idUsuario = 1)
('Tu receta "Lasaña vegetariana de berenjenas" fue aprobada.', 1),
('Tu receta "Cous cous con vegetales" está pendiente de aprobación.', 1),
('Recibiste una nueva calificación en "Lasaña vegetariana de berenjenas".', 1),
('Tu comentario fue aprobado en "Lasaña vegetariana de berenjenas".', 1),
('¡Tu receta "Tarta de Manzana" fue marcada como favorita!', 1),

-- Lucas Rojas (idUsuario = 2)
('Tu receta "Rissotto" fue aprobada.', 2),
('Recibiste una nueva calificación en "Rissotto".', 2),
('Tu comentario fue aprobado en "Rissotto".', 2),
('Tu receta "Brownies de Chocolate" fue aprobada.', 2),
('¡Tu receta "Brownies de Chocolate" fue marcada como favorita!', 2),

-- María López (idUsuario = 3)
('Tu receta "Mousse de chocolate" fue aprobada.', 3),
('Recibiste una nueva calificación en "Mousse de chocolate".', 3),
('Tu comentario fue aprobado en "Mousse de chocolate".', 3),
('Tu receta "Budín de Banana" está pendiente de aprobación.', 3),
('¡Tu receta "Budín de Banana" fue marcada como favorita!', 3),

-- Juan Pérez (idUsuario = 4)
('Tu receta "Cheescake de Frutilla" fue aprobada.', 4),
('Tu receta "Ensalada tibia de lentejas" está pendiente de aprobación.', 4),
('Recibiste una nueva calificación en "Cheescake de Frutilla".', 4),
('Tu comentario fue aprobado en "Cheescake de Frutilla".', 4),
('¡Tu receta "Pizza Margarita" fue marcada como favorita!', 4),

-- Carla Díaz (idUsuario = 5)
('Tu receta "Tarta de Manzana" fue aprobada.', 5),
('Recibiste una nueva calificación en "Tarta de Manzana".', 5),
('Tu comentario fue aprobado en "Tarta de Manzana".', 5),
('Tu receta "Empanadas de Espinaca" está pendiente de aprobación.', 5),
('¡Tu receta "Sandwich de Pollo" fue marcada como favorita!', 5),

('Bienvenido , gracias por registrarse.', 6),
('Bienvenido , gracias por registrarse.', 7),
('Bienvenido , gracias por registrarse.', 8),
('Bienvenido , gracias por registrarse.', 9),
('Bienvenido , gracias por registrarse.', 10),
('Bienvenido , gracias por registrarse.', 11),
('Bienvenido , gracias por registrarse.', 12),
('Bienvenido , gracias por registrarse.', 13),

-- Jorge Méndez (idUsuario = 14)
('Tu receta "Pizza Margarita" fue aprobada.', 14),
('Recibiste una nueva calificación en "Pizza Margarita".', 14),
('Tu comentario fue aprobado en "Pizza Margarita".', 14),
('Tu receta "Lasaña vegetariana de berenjenas" fue marcada como favorita.', 14),
('¡Tu receta "Lasaña vegetariana de berenjenas" fue marcada como favorita!', 14),

-- Valeria Suárez (idUsuario = 15)
('Tu receta "Sandwich de Pollo" fue aprobada.', 15),
('Recibiste una nueva calificación en "Sandwich de Pollo".', 15),
('Tu comentario fue aprobado en "Sandwich de Pollo".', 15),
('Tu receta "Cous cous con vegetales" fue marcada como favorita.', 15),
('¡Tu receta "Cous cous con vegetales" fue marcada como favorita!', 15),
('Bienvenido , gracias por registrarse.', 16),
('Bienvenido , gracias por registrarse.', 17),
('Bienvenido , gracias por registrarse.', 18),
('Bienvenido , gracias por registrarse.', 19),
('Bienvenido , gracias por registrarse.', 20),
('Bienvenido , gracias por registrarse.', 21),
('Bienvenido , gracias por registrarse.', 22),
('Bienvenido , gracias por registrarse.', 23),
('Bienvenido , gracias por registrarse.', 24),
('Bienvenido , gracias por registrarse.', 25);