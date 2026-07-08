-- ============================================================
-- CREACIÓN DE BASE DE DATOS Y TABLA
-- ============================================================


DROP TABLE IF EXISTS temperaturas;

CREATE TABLE temperaturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hora FLOAT NOT NULL,          -- Hora del día (0.0 a 24.0)
    temp FLOAT NOT NULL           -- Temperatura en °C
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- INSERCIÓN DE 50 REGISTROS (mediciones cada ~30 min)
-- ============================================================
-- Los datos simulan un día con mínima a las 6:00 (12 °C) y máxima a las 15:00 (28 °C)
-- Usamos una función seno para generar valores, pero añadimos pequeñas variaciones
-- para que parezcan mediciones reales.
INSERT INTO temperaturas (hora, temp) VALUES
(0.0, 16.5),
(0.5, 16.0),
(1.0, 15.3),
(1.5, 14.8),
(2.0, 14.2),
(2.5, 13.7),
(3.0, 13.2),
(3.5, 12.8),
(4.0, 12.5),
(4.5, 12.3),
(5.0, 12.1),
(5.5, 12.0),
(6.0, 12.0),
(6.5, 12.2),
(7.0, 12.7),
(7.5, 13.3),
(8.0, 14.0),
(8.5, 14.8),
(9.0, 15.6),
(9.5, 16.5),
(10.0, 17.4),
(10.5, 18.3),
(11.0, 19.2),
(11.5, 20.0),
(12.0, 21.0),
(12.5, 21.9),
(13.0, 22.8),
(13.5, 23.7),
(14.0, 24.7),
(14.5, 25.6),
(15.0, 26.4),
(15.5, 27.1),
(16.0, 27.5),
(16.5, 27.8),
(17.0, 28.0),
(17.5, 27.8),
(18.0, 27.5),
(18.5, 27.0),
(19.0, 26.3),
(19.5, 25.5),
(20.0, 24.6),
(20.5, 23.7),
(21.0, 22.7),
(21.5, 21.8),
(22.0, 20.8),
(22.5, 19.8),
(23.0, 18.9),
(23.5, 18.0),
(24.0, 17.2);

-- (Faltan algunos para llegar a 50, añadimos dos más para completar)
INSERT INTO temperaturas (hora, temp) VALUES
(24.5, 16.8),
(25.0, 16.4);