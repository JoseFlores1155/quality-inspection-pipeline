[README_quality_pipeline.md](https://github.com/user-attachments/files/28330170/README_quality_pipeline.md)

# Quality Inspection Pipeline 🏭

> Sistema de base de datos para gestión de inspecciones de primera pieza en manufactura industrial. Implementado en dos versiones: **SQLite** (local/portable) y **PostgreSQL** (producción). Detecta y reporta piezas rechazadas en tiempo real.

---

## ¿Qué problema resuelve?

En procesos de manufactura bajo norma ISO 9001:2015, el registro de inspecciones de "primera pieza" (dimensiones en mm, estatus de aprobación) se hacía de forma manual o en archivos dispersos. Este proyecto estructura esos registros en una base de datos relacional con reportes automáticos de piezas fuera de especificación.

---

## Arquitectura del proyecto

El sistema tiene dos scripts independientes según el entorno de despliegue:

| Script | Base de datos | Caso de uso |
|---|---|---|
| `inspecciones_de_primera_pieza.py` | SQLite (`fabrica.db`) | Local, sin servidor, portable |
| `posgretsql_productos_de_primera_pieza.py` | PostgreSQL | Producción, multi-usuario, escalable |

Ambos implementan el mismo flujo ETL:

```
Datos de producción (lista de tuplas)
        ↓
  DROP + CREATE TABLE   ← estructura limpia en cada ejecución
        ↓
  INSERT INTO (executemany)
        ↓
  SELECT WHERE estatus = 'Rechazado'
        ↓
  Reporte en consola
```

---

## Esquema de la base de datos

```sql
CREATE TABLE inspecciones (
    id     SERIAL PRIMARY KEY,   -- INTEGER AUTOINCREMENT en SQLite
    pieza  VARCHAR(100),         -- Nombre del componente inspeccionado
    medida_mm NUMERIC,           -- Dimensión medida (precisión en mm)
    estatus   VARCHAR(50)        -- 'Aprobado' | 'Rechazado'
);
```

> Tipos de datos diferenciados por motor: `SERIAL` en PostgreSQL vs `INTEGER AUTOINCREMENT` en SQLite. `NUMERIC` para garantizar precisión en medidas dimensionales.

---

## Tecnologías

| Herramienta | Uso |
|---|---|
| Python 3.x | Scripts de automatización |
| SQLite3 (`sqlite3`) | Base de datos local embebida, sin servidor |
| PostgreSQL | Base de datos relacional de producción |
| psycopg2 | Driver de conexión Python ↔ PostgreSQL |
| SQL | DDL (CREATE, DROP) y DML (INSERT, SELECT) |

---

## Estructura del proyecto

```
quality-inspection-pipeline/
│
├── inspecciones_de_primera_pieza.py          # Versión SQLite (local)
├── posgretsql_productos_de_primera_pieza.py  # Versión PostgreSQL (producción)
│
├── fabrica.db                                # Base de datos SQLite generada
│
└── README.md
```

---

## Cómo ejecutar

### Versión SQLite (sin configuración previa)

```bash
# Instalar dependencias (sqlite3 viene incluido en Python)
# No requiere instalación adicional

# Ejecutar
python inspecciones_de_primera_pieza.py
```

Genera automáticamente `fabrica.db` en el directorio actual.

---

### Versión PostgreSQL

```bash
# Instalar dependencias
pip install psycopg2-binary

# Configurar credenciales en el script (líneas 5-10)
conexion = psycopg2.connect(
    host="localhost",
    port="5432",
    database="postgres",
    user="postgres",
    password="TU_CONTRASEÑA"   # ← cambiar aquí
)

# Ejecutar
python posgretsql_productos_de_primera_pieza.py
```

> ⚠️ Requiere PostgreSQL instalado y corriendo en el puerto 5432.

---

## Output de ejemplo

```
¡Conexión exitosa a PostgreSQL!
Base de datos estructurada: Tabla 'inspecciones' creada.
¡Éxito total! Se insertaron 6 registros.

--- REPORTE DE PIEZAS RECHAZADAS ---
ID: 2 | Pieza: Engrane A   | Medida: 12.1mm | Estado: Rechazado
ID: 5 | Pieza: Engrane A   | Medida: 11.8mm | Estado: Rechazado

Conexión cerrada. El script terminó correctamente.
```

---

## Datos de muestra incluidos

| Pieza | Medida (mm) | Estatus |
|---|---|---|
| Eje Central | 25.4 | ✅ Aprobado |
| Engrane A | 12.1 | ❌ Rechazado |
| Eje Central | 25.5 | ✅ Aprobado |
| Soporte Lateral | 45.0 | ✅ Aprobado |
| Engrane A | 11.8 | ❌ Rechazado |
| Placa Base | 100.2 | ✅ Aprobado |

---

## Decisiones técnicas destacadas

- **`executemany()`** en lugar de múltiples `execute()` — inserción eficiente de lotes de registros
- **`DROP TABLE IF EXISTS`** antes de `CREATE TABLE` — garantiza una ejecución limpia y reproducible
- **Manejo de errores en PostgreSQL** — bloque `try/except` con codificación ASCII para evitar errores de encoding en mensajes de PostgreSQL
- **Cierre explícito de conexión** — `cursor.close()` + `conexion.close()` para liberar recursos correctamente

---

## Contexto industrial

Desarrollado durante práctica profesional como Data Scientist aplicado a Gestión de Calidad (Jun 2024 – Ene 2025). Basado en los flujos reales de inspección de primera pieza bajo normativa ISO 9001:2015, donde la trazabilidad y precisión dimensional de cada componente es requisito de auditoría.

---

> Los datos incluidos son de muestra. No contienen registros reales de producción de ninguna empresa.
