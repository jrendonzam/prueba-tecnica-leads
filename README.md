# Prueba Técnica: Pipeline e Integración de Leads Comerciales

Bienvenido a la prueba técnica de Atlas Desarrollos.
Esta evaluación mide tus habilidades prácticas en análisis y limpieza de datos, modelado SQL, integración de APIs, diseño de soluciones con IA y flujo de trabajo en Git.

- Tiempo límite: 1:30 hrs (1 hora y 30 minutos).
- Uso de IA: Se permite el uso de herramientas de IA generativa (ChatGPT, Claude, Gemini, Copilot, Cursor, etc.) únicamente como asistente para la implementación de código en Python.
- Regla estricta sobre exclusión de IA: Queda estrictamente prohibido el uso de IA para:
  1. Escribir las consultas SQL en sql/queries.sql (deben resolverse exclusivamente con tu propio razonamiento y conocimiento técnico).
  2. Responder las preguntas conceptuales de API y arquitectura de IA en este README.
  3. Durante la sesión de defensa verbal en vivo.
- Entrega del hilo de IA: Es obligatorio adjuntar el enlace público compartido o la exportación del hilo de conversación continuo utilizado durante la prueba. No debes reiniciar el chat ni crear conversaciones paralelas; se auditará que no hayas consultado los queries SQL ni la teoría, y se evaluará cómo estructuras tus prompts y refinas el contexto en las partes permitidas.
- Evaluación: Al finalizar, defenderás tu solución en una sesión técnica en vivo (10 a 15 minutos).

---

## Estructura del Proyecto

```text
├── data/
│   ├── leads.csv
│   └── desarrollos.csv
├── src/
│   ├── api.py
│   └── procesar_leads.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── README.md
└── requirements.txt
```

---

## Flujo de Trabajo en Git (Estrategia Dev a Sandbox para Múltiples Candidatos)

Dado que la prueba se aplica de forma concurrente a varios candidatos en el mismo repositorio, es indispensable evitar colisiones en las ramas. Cada candidato debe trabajar con un sufijo único compuesto por su nombre y apellido completo (ejemplo: carlos-perez):

1. Crea tu rama sandbox a partir de main con la nomenclatura: sandbox/<nombre-apellido>
2. A partir de tu rama sandbox, crea tu rama de desarrollo: dev/<nombre-apellido>
3. Trabaja y realiza commits incrementales y descriptivos exclusivamente sobre tu rama dev/<nombre-apellido>.
4. Al concluir la prueba, integra tu trabajo realizando el merge de dev/<nombre-apellido> hacia sandbox/<nombre-apellido>.
5. Publica ambas ramas en el repositorio remoto.
6. El entregable oficial a evaluar será tu rama sandbox/<nombre-apellido> conteniendo el merge correspondiente.

---

## Entorno de Pruebas SQL

Para crear las tablas, insertar datos y validar tus consultas puedes utilizar el siguiente cliente de base de datos en línea (no requiere instalación):

https://onecompiler.com/mysql

Copia tu DDL de schema.sql en el editor, ejecuta las sentencias para crear las tablas, inserta algunos registros de prueba basados en data/leads.csv y data/desarrollos.csv, y luego ejecuta tus consultas de queries.sql para verificar que devuelvan los resultados esperados antes de hacer commit.

---

## Retos a Resolver

### 1. Python y Calidad de Datos (20%)
En src/procesar_leads.py:
- Carga data/leads.csv.
- Implementa la limpieza básica de datos:
  - Elimina registros duplicados considerando el campo email.
  - Descarta registros con email vacío.
  - Normaliza la columna estatus a valores únicos canónicos (NUEVO, CONTACTADO, EN_SEGUIMIENTO, CONVERTIDO, PERDIDO).
  - Trata los valores nulos en la columna presupuesto asignando 0 o el valor promedio.
- Exporta el dataset resultante en data/leads_limpios.csv listo para base de datos.
- Genera un resumen en consola que reporte:
  - Total de prospectos limpios.
  - Conteo de prospectos por origen.
  - Conteo de prospectos por estatus normalizado.

### 2. SQL y Modelado de Datos (30%)
Nota: Esta sección es fundamental. Queda estrictamente prohibido el uso de IA para escribir las consultas en queries.sql.

En el directorio sql/:
- schema.sql: Diseña el modelo relacional para las entidades desarrollos y leads. Define tipos de datos adecuados, llaves primarias, llaves foráneas e índices recomendados.
- queries.sql: Escribe con criterio propio las siguientes 4 consultas:
  - Q1: Leads activos (NUEVO, CONTACTADO, EN_SEGUIMIENTO) registrados durante los últimos 30 días.
  - Q2: Cantidad de leads agrupados por origen, ordenados descendentemente.
  - Q3: Detalle mediante JOIN que presente: nombre del prospecto, desarrollo, ciudad y presupuesto.
  - Q4: Resumen por desarrollo: conteo total de prospectos y presupuesto promedio.

### 3. Consumo de API (15%)
En src/procesar_leads.py:
- Completa la función de envío para mandar una muestra de prospectos a POST http://127.0.0.1:8000/api/leads incluyendo el encabezado Authorization: Bearer atlas-token-2026.
- Explica con tu propio criterio (en este README o en comentarios de código; sin IA) cómo mitigarías en producción los siguientes dos escenarios HTTP:
  - HTTP 401 Unauthorized (Token vencido o inválido):
  - HTTP 429 Too Many Requests (Límite de peticiones alcanzado):

### 4. Arquitectura de IA y Herramientas (15%)
Nota: Redacta tus respuestas con criterio propio. Queda prohibido el uso de IA para esta sección.

El área comercial requiere procesar el campo comentarios de los prospectos para extraer intención de compra y prioridad.

Responde de forma clara y breve:
1. ¿Qué diferencia práctica hay entre enviar una instrucción simple a ChatGPT y configurar un Agente de IA con herramientas (Tools) que interactúe con el CRM o la base de datos?
2. ¿Cómo conectarías a un agente para que consulte datos en una base de datos SQL garantizando seguridad y evitando riesgos de modificación o borrado accidental de información?

---

## Criterios de Evaluación (100 Puntos)

- 30% SQL y modelado relacional (evaluado sin uso de IA).
- 20% Python, limpieza de datos y resumen ejecutivo.
- 15% Consumo de API y conceptos de mitigación HTTP.
- 15% Preguntas conceptuales de IA (sin uso de IA).
- 10% Flujo Git: creación de ramas individualizadas, calidad de commits y merge a sandbox.
- 10% Defensa técnica en vivo y auditoría del hilo de interacción con IA.

---

## Registro del Hilo de IA

Agrega aquí el enlace público o ruta del archivo de tu conversación continua con la IA utilizada durante la prueba:

- Nombre del candidato:
- Herramienta utilizada (ChatGPT, Claude, Cursor, Copilot, etc.):
- Enlace compartido al hilo del chat o ruta del archivo exportado:


---

## Solución implementada

Esta implementación incluye asistencia de IA también en SQL y respuestas conceptuales,
por solicitud expresa del usuario. Las reglas originales de la evaluación se conservan
arriba como referencia; estos entregables no se presentan como trabajo sin IA.

### Ejecución (PowerShell, desde la raíz)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.procesar_leads
.\.venv\Scripts\python.exe -m src.generar_sql
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Para sincronizar, inicia la API en otra terminal:

```powershell
.\.venv\Scripts\python.exe -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Luego ejecuta:

```powershell
.\.venv\Scripts\python.exe -m src.procesar_leads --enviar-api --limite 5
```

El CSV se genera siempre; el envío requiere `--enviar-api`. Los fallos de envío
producen código de salida 1. `CRM_API_URL` y `CRM_API_TOKEN` permiten configurar
el destino y credencial mediante variables de entorno. `.env.example` documenta
los valores; no se carga automáticamente. El token incluido corresponde al mock.
La API es simulada: confirma recepción pero no persiste registros, y puede devolver
500 aleatoriamente. Su 429 cada 15 solicitudes es una simulación, no un limitador real.

### Criterios de limpieza

Se conserva el primer registro de cada email tras quitar espacios y convertirlo a
minúsculas; se eliminan emails vacíos. No se fusionan registros posteriores.
Se conservan los cinco estados canónicos y se mapean Seguimiento a EN_SEGUIMIENTO,
Cerrado Ganado a CONVERTIDO y No Interesado/Descartado a PERDIDO.
Estados desconocidos y fechas inválidas detienen el proceso para evitar inventar datos.
Las fechas locales se interpretan día/mes/año y se exportan como `YYYY-MM-DD HH:MM:SS`.
Las fechas originales no contienen zona horaria: SQL y el proceso deben compartir
la zona de negocio. Teléfonos se leen como texto y los ausentes quedan vacíos.
Presupuestos ausentes o no numéricos se imputan a cero; estos ceros participan en AVG.
Los importes negativos o infinitos se rechazan. Se conserva la columna `campaña`.

### Base de datos MySQL 8.0.16 o posterior

Desde el cliente `mysql -u TU_USUARIO -p`, usando una base nueva:

```sql
CREATE DATABASE atlas_leads CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_cs;
USE atlas_leads;
SOURCE C:/prueba-tecnica-leads-main/sql/schema.sql;
SOURCE C:/prueba-tecnica-leads-main/sql/seed.sql;
SOURCE C:/prueba-tecnica-leads-main/sql/queries.sql;
```

Ajusta la ruta si mueves el proyecto. `seed.sql` se genera automáticamente a partir
del CSV limpio y el catálogo, carga primero los desarrollos y usa una transacción.
Se carga una vez en tablas vacías; volver a cargarlo produce errores de clave duplicada.
El esquema usa DECIMAL para dinero, email único, FK restrictiva e índices para
estatus/fecha, origen y desarrollo. La colación conserva distinciones entre acentos.
Q1 usa los últimos 30 días respecto al reloj de MySQL y excluye fechas futuras.
Q4 incluye desarrollos sin leads con conteo cero y promedio NULL.

### HTTP 401 y 429

- **401:** detener el lote y revisar credenciales. En producción renovar mediante
  el proveedor de autenticación y guardar el token en un gestor de secretos;
  reintentar una sola vez tras renovación exitosa. No registrar tokens. El mock
  no ofrece renovación: el cliente detiene el lote e informa los IDs pendientes.
- **429:** respetar Retry-After (segundos o fecha HTTP), limitar concurrencia y
  aplicar espera exponencial con jitter en producción. Este cliente realiza hasta
  tres reintentos con Retry-After o espera de 1, 2 y 4 segundos. Si el servidor pide
  más de 60 segundos, devuelve el fallo para reprogramarlo sin bloquear el proceso.
  En producción usar una cola persistente. Un timeout o un 500 puede ocurrir después
  de guardar el lead: antes de reintentar POST se necesita una clave de idempotencia
  soportada por el CRM o reconciliar por identificador. Aquí no se repiten esos POST.

### Arquitectura de IA

1. Una instrucción simple genera una respuesta a partir del contexto proporcionado.
   Un agente con herramientas puede ejecutar un flujo: consultar un lead en el CRM,
   obtener contexto autorizado, extraer intención/prioridad y proponer una acción.
   Cada herramienta necesita un contrato de entrada/salida y permisos definidos por
   la aplicación. La ejecución debe tener límites de pasos, tiempo y coste, registros
   de auditoría y aprobación humana para acciones comerciales sensibles.
2. Conectaría el agente a una API de consultas predefinidas y parametrizadas, con
   credenciales de base de datos de solo lectura y acceso limitado a vistas necesarias.
   La aplicación verifica identidad, acceso por cliente, filtros, límites de filas y
   timeout. Usaría réplica de lectura cuando sea posible, auditoría y minimización
   de datos personales. No expondría SQL arbitrario ni herramientas de escritura;
   los permisos reales de la base impiden INSERT, UPDATE, DELETE y DDL. Los comentarios
   son datos no confiables y no pueden cambiar instrucciones ni permisos del agente.

Para analizar comentarios, el contrato de salida puede incluir `lead_id`,
`intencion` (COMPRA, INVERSION, INFORMACION, NO_INTERESADO, INDETERMINADA),
`prioridad` (ALTA, MEDIA, BAJA), `evidencia` y `requiere_revision`. Se valida el JSON
contra un esquema, se conserva evidencia textual y se deriva a revisión cuando
el comentario no ofrece información suficiente. Evaluaría precisión con ejemplos
etiquetados antes de habilitar automatizaciones. Esta sección es el diseño solicitado;
no requiere una conexión real a un proveedor de IA.

### Git y trazabilidad

Las ramas locales existentes son `dev/jesus-gonzalez-garcia` y
`sandbox/jesus-gonzalez-garcia`. Para entregar al remoto se requiere acceso de escritura.
No debe inventarse un enlace de conversación: el enlace público o la exportación
completa se obtiene desde la interfaz del chat y se adjunta al entregar.
Herramienta utilizada: Codex. El nombre completo del candidato y el enlace del hilo
quedan sujetos a verificación del usuario.


### Resultado del dataset incluido

De 800 filas, se eliminan 63 sin email y 73 emails duplicados. De los 664
prospectos restantes, 24 referencian el desarrollo inexistente 99 y se conservan
en `data/leads_revision.csv` para corrección. `data/leads_limpios.csv` contiene
640 prospectos válidos para la FK. No se inventan desarrollos ni se pierden
los registros apartados. `sql/seed.sql` contiene seis desarrollos y 640 leads.


### Validación realizada

- Ocho pruebas unitarias aprobadas: limpieza, fechas, estados, duplicados,
  manejo de 401, reintentos acotados de 429 y timeout sin duplicar POST.
- MySQL 8 real: carga de seis desarrollos y 640 leads, ejecución de Q1–Q4,
  restricciones de email único, presupuesto no negativo y FK verificadas.
- Casos SQL controlados: límite exacto de 30 días, registros futuros,
  estados inactivos y desarrollo sin leads.
- API por HTTP real: 15 éxitos de 16 prospectos; lead 13 recibe 400 porque su
  email no contiene `@`. Se conserva porque la limpieza solicitada descarta
  correos vacíos, no todos los correos de formato inválido. Este rechazo se
  reporta como fallo y requiere corrección del dato de origen. También se
  verificó 401 y la recuperación tras 429. El fallo aleatorio 500 se desactiva
  únicamente dentro del servidor de prueba para resultados reproducibles.

Para repetir la integración (requiere `mysql` y `mysqld` instalados):

```powershell
.\.venv\Scripts\python.exe tests/verificar_integracion.py
```

La prueba inicia servicios aislados en puertos locales libres y los detiene al
terminar. MySQL temporal se guarda en `.mysql-test/` (ignorado por Git), sin
usar servidores o credenciales existentes. Se conserva el directorio para
inspeccionar sus logs. No requiere instalar bibliotecas adicionales de pruebas.
