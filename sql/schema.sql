-- =============================================================
-- SECCIÓN 2.1: Modelado de Datos (DDL)
-- =============================================================
-- Instrucciones:
-- Escribe las sentencias CREATE TABLE para almacenar 'desarrollos' y 'leads'.
-- Considera llaves primarias, foráneas, tipos de datos e índices recomendados.

CREATE TABLE desarrollos (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    ciudad VARCHAR(50),
);


CREATE TABLE leads (
    id INT PRIMARY KEY,
    nombre_prospecto VARCHAR(100),
    id_desarrollo INT,
    origen VARCHAR(50),
    estatus VARCHAR(30),
    presupuesto DECIMAL(12, 2),
    fecha_registro DATE,
    foreign key (id_desarrollo) references desarrollos(id)
);

CREATE INDEX index_leads_estatus ON leads(estatus);
CREATE INDEX index_leads_origen ON leads(origen);
CREATE INDEX index_leads_fecha ON leads(fecha_registro);
CREATE INDEX index_leads_desarrollo ON leads(id_desarrollo);
