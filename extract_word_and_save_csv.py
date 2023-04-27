# obtengo una lista de de archivos word 
# a partir del directorio Desktop leyendo sus subdirectorios
# los corto en largos de varios parrafos
# hasta completar 500 letras, y los guardo en un csv
# ----------------------------------------------------------
import os, csv, docx

print("--- leo una lista de parrafos de los archivos que encuentre ---")
file_name = "mis_word.csv"
# Open the file in write mode
with open(file_name, mode='w', newline='', encoding='utf-8') as file:
  # Create a CSV writer object
  writer = csv.writer(file)

  qparrafos = 0
  row = []
  #list of the full paths to all Word files in the directory and subdirectories
  directory = "/Users/stjepan/Desktop"
  for root, directories, files in os.walk(directory):
    for file in files:
      # los archivos temporales empiezan con "~$" y son ilegibles
      # lo intento solamente con los docx, no con los doc, pero quizas funcione
      if file.endswith(".docx") and not file.startswith("~$"):
        print(root, directory, file)
        with open(root+"/"+file, "rb") as f:
          word_document = docx.Document(f)

        texto_del_parrafo = ""
        letras_del_parrafo = 0
        # el lector word no lee paginas, sino parrafos
        for parrafo in word_document.paragraphs:
          texto = parrafo.text
          letras_del_parrafo += len(texto)
          # las lineas en blanco tienen largo 0, mejor les pongo algunos espacios
          if len(texto) == 0:
             texto = "         "
          texto_del_parrafo += texto
          # si la cantidad de letras excede un numero escribo y reinicializo
          if letras_del_parrafo > 500:
             qparrafos += 1
             row.append(qparrafos)
             row.append(f.name)
             row.append(texto_del_parrafo)
             # cada linea tiene: nro de parrafo, nombre de archivo, texto
             writer.writerow(row)
             row = []
             texto_del_parrafo= ""
             letras_del_parrafo = 0

print("--- cantidad de parrafos = ", qparrafos, " ---")
