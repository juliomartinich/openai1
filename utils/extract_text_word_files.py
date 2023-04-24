import os
import docx

directory = "/Users/stjepan/Desktop"
#list of the full paths to all Word files in the directory.
archivos = []
textos = []
qparrafos = 0
print("---")
for root, directories, files in os.walk(directory):
  for file in files:
    if file.endswith(".docx") and not file.startswith("~$"):
      print(root, directory, file)
      with open(root+"/"+file, "rb") as f:
        word_document = docx.Document(f)

      texts = ""
      i = 0
      letras = 0
      for parrafo in word_document.paragraphs:
        i += 1
        text = parrafo.text
        letras += len(text)
        if len(text) == 0:
           text = "\n"
        texts = texts + text
        if letras > 500:
           qparrafos += 1
           archivos.append(f.name)
           textos.append(texts)
           texts = ""
           letras = 0

print("Parrafos = ", qparrafos)
for archivo in archivos:
  print(archivo)
print("---")
