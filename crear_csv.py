import csv
import MySQLdb
import sys
import os
import time

inicio = time.time()
# conexión a la base de datos
try:
    db = MySQLdb.connect("localhost", "root", "", "base_prueba")
except MySQLdb.Error as e:
    print("No puedo conectar a la base de datos:", e)
    sys.exit(1)

# declaramos nuestro cursor para poder hacer consultas a la base de datos
cursor = db.cursor()

# Verificar si el directorio 'csv' existe, y crearlo si no
if not os.path.exists('csv'):
    os.makedirs('csv')

# Crear archivos CSV por provincia.
try:
    # recuperamos los valores únicos de la columna provincia
    cursor.execute("SELECT DISTINCT provincia FROM emp")
    # recibimos todas las provincias 
    provincias = cursor.fetchall()
    for provincia in provincias:
        cursor.execute("SELECT * FROM emp WHERE provincia = %s", (provincia[0],))
        # obtenemos 
        localidades = cursor.fetchall()
        with open(f"csv/Localidades de {provincia[0]}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Escribir filas de datos
            writer.writerows(localidades)

            # Obtener la cantidad de localidades y escribirla al final del archivo CSV
            cantidad_localidades = len(localidades)
            writer.writerow([])  # Agregar una fila vacía como separador
            writer.writerow(["Cantidad de Localidades: " + str(cantidad_localidades)])
except MySQLdb.Error as e:
    db.rollback()
    print("Error al ejecutar la consulta SQL:", e)
finally:
    cursor.close()
    db.close()

print("Archivos CSV creados con éxito")
fin = time.time()

duracion = fin - inicio
print(f"Tiempo de ejecución: {duracion} segundos")