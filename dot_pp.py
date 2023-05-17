import csv

def dot_product(vector1, vector2):
    # Calcula el producto punto entre dos vectores.
    if len(vector1) != len(vector2):
        raise ValueError("Los dos vectores deben tener la misma longitud.")

    dot_product = sum(x * y for x, y in zip(vector1, vector2))
    return dot_product

archivo_uno = "catalogo_preguntas_embed.csv"
archivo_dos = "mis_word_embed.csv"
archivo_tres = "cruz_preguntas_parrafos.csv"

with open(archivo_uno, newline='') as csv_uno, \
     open(archivo_dos, newline='') as csv_dos, \
     open(archivo_tres, 'w', newline='') as csv_tres:

    lector_uno = csv.reader(csv_uno)
    lector_dos = csv.reader(csv_dos)
    escritor_tres = csv.writer(csv_tres)

    for fila_uno in lector_uno:
        pregunta_texto = fila_uno.pop()
        pregunta_usr   = fila_uno.pop()
        pregunta_nro   = fila_uno.pop()
        fila_uno = [float(x) for x in fila_uno]  # Convierte los valores a números flotantes
        resultados_fila = [pregunta_nro, pregunta_usr, pregunta_texto]
        for fila_dos in lector_dos:
            parrafo_texto = fila_dos.pop()
            parrafo_arch  = fila_dos.pop()
            parrafo_nro   = fila_dos.pop()
            fila_dos = [float(x) for x in fila_dos]  # Convierte los valores a números flotantes
            producto_punto = round(1000*dot_product(fila_uno, fila_dos))
            resultados_fila.append(producto_punto)

        escritor_tres.writerow(resultados_fila)
        csv_dos.seek(0)  # Reinicia el lector del archivo dos.csv al inicio

print("El producto punto vectorial se ha calculado y almacenado en el archivo tres.csv.")

