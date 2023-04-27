obtiene_embeddings: busca embeddings desde una lista de animales fija
                    entrega el archivo vectores_de_anuimales.csv

compara_embeddings: compara los embeddings entre si, todos con todos
                    leyendo el archivo vectores_de_animales.csv
                    haciendo el producto punto de todas las combinaciones
                    entrega los mas parecidos por pantalla

-------------------------------------------------------------------------

extract_word_and_save_csv.py:
		a partir del Desktop, busca los archivos word
		cada uno lo corta en parrafos hasta que se supere 500 letras
		guarda en archivo:
		mis_word.csv
		- la secuencia del bloque de parrafos
		- la ruta y nombre de cada archivo
                - el texto

csv_read_and_embed.py
		a partir del archivo anterior
		calcula embeddings para cada bloque
                entrega en archivo:
		mis_word_embed.csv
		- vector de embeddings
		+ lo mismo que venía en el archivo:
		- la secuencia del bloque de parrafos
		- la ruta y nombre de cada archivo
                - el texto
		
busca_word_mas_cercano.py
		pide ingresar un texto
                calcula su embedding
		busca en los bloques el parrafo mas cercano semanticamente
                lo entrega por pantalla

chatbot_misword.py
		pide ingresar una pregunta
		calcula su embedding
		busca en los bloques el parrafo mas cercano semanticamente
                le pide a chatGPT que elabore una respesta a la pregunta
		basado en el texto del bloque mas cercano semanticamente encontrado
                si encuentra que no esta relacionado
		le pide que conteste que no tiene esa informacion
		
