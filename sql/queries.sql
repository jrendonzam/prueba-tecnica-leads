-- =============================================================
-- SECCIÓN 2.2: Consultas SQL
-- REGLA ESTRICTA: Las consultas deben ser escritas con criterio
-- y conocimiento propio. Queda prohibido el uso de IA en esta sección.
-- =============================================================

-- Consulta 1 (Filtro básico de fecha y estado):
SELECT id, nombre,fecha_registro, estado
FROM usuarios
WHERE estatus ='0'
-- Obtén todos los leads activos (NUEVO, CONTACTADO, EN_SEGUIMIENTO) registrados en los últimos 30 días.
SELECT id, nombre,

-- Consulta 2 (Agregación y ordenamiento):
-- Obtén la cantidad de leads agrupados por origen, ordenados de mayor a menor.


-- Consulta 3 (JOIN relacional):
-- Obtén el nombre del prospecto, nombre del desarrollo, ciudad y presupuesto.


-- Consulta 4 (Métricas de Negocio):
-- Obtén por desarrollo: total de prospectos y presupuesto promedio.

