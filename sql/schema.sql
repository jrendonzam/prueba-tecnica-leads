-- =============================================================
-- SECCIÓN 2.1: Modelado de Datos (DDL)
-- =============================================================
-- Instrucciones:
-- Escribe las sentencias CREATE TABLE para almacenar 'desarrollos' y 'leads'.
-- Considera llaves primarias, foráneas, tipos de datos e índices recomendados.

-- CREATE TABLE desarrollos (...);

-- CREATE TABLE leads (...);
--Yo primero lo compile en onecompiler.com despues de probar que no me diera error ya lo pegue aqui tambien quite la ñ de la columna campaña para no afectar la bd y mantener un estandard... 
CREATE TABLE leads (
    id INT PRIMARY KEY,
    nombre VARCHAR(255),
    email VARCHAR(50),
    telefono VARCHAR(20),
    origen VARCHAR(100),
    campana VARCHAR(50),
    fecha_registro DATETIME,
    estatus VARCHAR(30),
    presupuesto DECIMAL(12, 2),
    desarrollo_id INT,
    comentarios TEXT
);

CREATE TABLE desarrollos(
  id INT PRIMARY KEY,
  nombre VARCHAR(255),
  ciudad VARCHAR(255),
  estado VARCHAR(255)
)