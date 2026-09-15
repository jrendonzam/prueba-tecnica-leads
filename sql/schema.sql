-- MySQL 8.0.16+. Ejecutar dentro de una base de datos seleccionada.
CREATE TABLE IF NOT EXISTS desarrollos (
    id INT UNSIGNED PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    estado VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_cs;

CREATE TABLE IF NOT EXISTS leads (
    id INT UNSIGNED PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    telefono VARCHAR(30) NOT NULL DEFAULT '',
    origen VARCHAR(100) NOT NULL,
    `campaña` VARCHAR(100),
    fecha_registro DATETIME NOT NULL,
    estatus ENUM('NUEVO','CONTACTADO','EN_SEGUIMIENTO','CONVERTIDO','PERDIDO') NOT NULL,
    presupuesto DECIMAL(14,2) NOT NULL DEFAULT 0,
    desarrollo_id INT UNSIGNED NOT NULL,
    comentarios TEXT,
    CONSTRAINT uq_leads_email UNIQUE (email),
    CONSTRAINT chk_presupuesto CHECK (presupuesto >= 0),
    CONSTRAINT fk_leads_desarrollo FOREIGN KEY (desarrollo_id)
        REFERENCES desarrollos(id) ON UPDATE RESTRICT ON DELETE RESTRICT,
    INDEX idx_leads_estatus_fecha (estatus, fecha_registro),
    INDEX idx_leads_origen (origen),
    INDEX idx_leads_desarrollo (desarrollo_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_cs;
