import os
import psycopg2
import sys

# 1. Intentar conectar a PostgreSQL con tus datos reales
try:
    conexion = psycopg2.connect(
        host="localhost",
        port="5432",          # mi puerto activo
        database="postgres",
        user="postgres",
        password=os.getenv("DB_PASSWORD", "")     # mi contraseña
    )
    print("¡Conexión exitosa a PostgreSQL!")
    
except Exception as e:
    error_limpio = str(e).encode('ascii', 'ignore').decode('ascii')
    print("\n[ERROR DE CONEXIÓN]:")
    print(error_limpio)
    sys.exit()

# 2. Crear el cursor para ejecutar comandos SQL
cursor = conexion.cursor()

# 3. Crear la tabla de inspecciones de calidad
cursor.execute("DROP TABLE IF EXISTS inspecciones;")

cursor.execute("""
CREATE TABLE inspecciones (
    id SERIAL PRIMARY KEY,
    pieza VARCHAR(100),
    medida_mm NUMERIC,
    estatus VARCHAR(50)
);
""")
conexion.commit()
print("Base de datos estructurada: Tabla 'inspecciones' creada.")

# 4. Insertar los datos simulados de producción
datos_produccion = [
    ('Eje Central', 25.4, 'Aprobado'),
    ('Engrane A', 12.1, 'Rechazado'),
    ('Eje Central', 25.5, 'Aprobado'),
    ('Soporte Lateral', 45.0, 'Aprobado'),
    ('Engrane A', 11.8, 'Rechazado'),
    ('Placa Base', 100.2, 'Aprobado')
]

cursor.executemany("""
INSERT INTO inspecciones (pieza, medida_mm, estatus) 
VALUES (%s, %s, %s);
""", datos_produccion)

conexion.commit()
print(f"¡Éxito total! Se insertaron {len(datos_produccion)} registros.")

# 5. Hacer una consulta rápida para validar en la terminal
cursor.execute("SELECT * FROM inspecciones WHERE estatus = 'Rechazado';")
piezas_defectuosas = cursor.fetchall()

print("\n--- REPORTE DE PIEZAS RECHAZADAS ---")
for fila in piezas_defectuosas:
    print(f"ID: {fila[0]} | Pieza: {fila[1]} | Medida: {fila[2]}mm | Estado: {fila[3]}")

# Cerrar las conexiones limpiamente
cursor.close()
conexion.close()
print("\nConexión cerrada. El script terminó correctamente.")
