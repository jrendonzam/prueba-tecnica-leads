-- Q1: Ventana móvil de 30 días, excluyendo registros futuros.
SELECT *
FROM leads
WHERE estatus IN ('NUEVO', 'CONTACTADO', 'EN_SEGUIMIENTO')
  AND fecha_registro >= NOW() - INTERVAL 30 DAY
  AND fecha_registro <= NOW()
ORDER BY fecha_registro DESC, id;

-- Q2: Desempate determinista por origen.
SELECT origen, COUNT(*) AS total_leads
FROM leads
GROUP BY origen
ORDER BY total_leads DESC, origen;

-- Q3: Detalle comercial.
SELECT l.nombre AS prospecto, d.nombre AS desarrollo, d.ciudad, l.presupuesto
FROM leads AS l
JOIN desarrollos AS d ON d.id = l.desarrollo_id
ORDER BY l.id;

-- Q4: Incluye desarrollos sin leads (conteo 0, promedio NULL).
SELECT d.id, d.nombre AS desarrollo, COUNT(l.id) AS total_prospectos,
       ROUND(AVG(l.presupuesto), 2) AS presupuesto_promedio
FROM desarrollos AS d
LEFT JOIN leads AS l ON l.desarrollo_id = d.id
GROUP BY d.id, d.nombre
ORDER BY total_prospectos DESC, d.id;
