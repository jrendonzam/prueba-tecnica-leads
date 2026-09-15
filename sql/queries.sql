-- =============================================================
-- SECCIÓN 2.2: Consultas SQL
-- REGLA ESTRICTA: Las consultas deben ser escritas con criterio
-- y conocimiento propio. Queda prohibido el uso de IA en esta sección.
-- =============================================================

-- Consulta 1 (Filtro básico de fecha y estado):
-- Obtén todos los leads activos (NUEVO, CONTACTADO, EN_SEGUIMIENTO) registrados en los últimos 30 días.
SELECT * FROM leads
WHERE estatus IN ('NUEVO', 'CONTACTADO', 'EN_SEGUIMIENTO')
AND fecha_registro >= CURRENT_DATE - INTERVAL 30 DAY;

-- Consulta 2 (Agregación y ordenamiento):
-- Obtén la cantidad de leads agrupados por origen, ordenados de mayor a menor.
SELECT origen, COUNT(*) AS cantidad_leads
FROM leads
GROUP BY origen
ORDER BY cantidad_leads DESC;

-- Consulta 3 (JOIN relacional):
-- Obtén el nombre del prospecto, nombre del desarrollo, ciudad y presupuesto.
SELECT l.nombre_prospecto, d.nombre AS nombre_desarrollo, d.ciudad, l.presupuesto
FROM leads l
JOIN desarrollos d ON l.id_desarrollo = d.id;

-- Consulta 4 (Métricas de Negocio):
-- Obtén por desarrollo: total de prospectos y presupuesto promedio.
SELECT d.nombre AS nombre_desarrollo, COUNT(l.id) AS total_prospectos, AVG(l.presupuesto) AS presupuesto_promedio
FROM desarrollos d
JOIN leads l ON d.id = l.id_desarrollo
GROUP BY d.nombre;
