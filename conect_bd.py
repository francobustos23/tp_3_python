import csv
import sys
import MySQLdb
import time

inicio = time.time()
# Abrir el archivo CSV
with open('localidades.csv', newline='', encoding="utf-8") as file:
    lector_csv = csv.reader(file, delimiter=',', quotechar='"')
    # Saltamos la primer fila que es el encabezado
    next(lector_csv)
    # Leer cada fila del CSV y guardar los datos en una lista de tuplas
    # ya que si queremos insertar varios datos a la vez hay que pasarlo en una lista de tuplas
    valores = []
    # iteramos todas las filas y las vamos agregando a la lista
    # luego transformamos las filas en tuplas
    for fila in lector_csv:
        valores.append(tuple(fila))
# Conexion a la base de datos
try:
    db = MySQLdb.connect("localhost", "root", "", "base_prueba")
except MySQLdb.Error as e:
    print("No puedo conectar a la base de datos:", e)
    sys.exit(1)

# Declaramos nuestro cursor para poder hacer consultas a la base de datos
cursor = db.cursor()

# Borrar la tabla si existe
cursor.execute("DROP TABLE IF EXISTS emp")
print("Tabla 'emp' eliminada (si existía).")

# Crear la tabla emp si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS emp (
        provincia VARCHAR(50),
        id INT,
        localidad VARCHAR(50),
        cp INT,
        id_prov_mstr INT
    )
""")
print("Tabla 'emp' creada o existente.")

# Realizar inserción de datos
sql = "INSERT INTO emp (provincia, id, localidad, cp, id_prov_mstr) VALUES (%s, %s, %s, %s, %s)"
# Enviamos la consulta a la base de datos
try:
    cursor.executemany(sql, valores)
    db.commit()
    print("Datos insertados correctamente")
except Exception as e:
    print("Error al insertar los datos:", e)
    db.rollback()

db.close()

fin = time.time()

duracion = fin - inicio
print(f"Tiempo de ejecución: {duracion} segundos")