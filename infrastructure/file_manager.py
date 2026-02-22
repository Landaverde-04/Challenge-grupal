import csv
import os

class FileManager:
    def __init__(self, archivo_nombre, fieldnames):
        self.archivo_path = f"data/{archivo_nombre}"
        self.fieldnames = fieldnames
        self._inicializar_archivo()

    def _inicializar_archivo(self):
        # Verificar si el directorio "data" existe, si no, crearlo
        if not os.path.exists("data"):
            os.makedirs("data")
        # Verificar si el archivo existe, si no, crearlo con los encabezados
        if not os.path.exists(self.archivo_path):
            with open(self.archivo_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()

    #Metodo para leer los datos del archivo CSV y devolverlos como una lista de diccionarios
    def leer_todos(self):
        #Lista vacia para almacenar los datos leidos del archivo CSV
        data =  []
        if os.path.exists(self.archivo_path):
            with open(self.archivo_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
        return data
    
    #Metodo para escribir un nuevo registro en el archivo CSV
    def agregar(self, registro_dict): #aca le paso un diccionario con los datos del nuevo registro
        with open(self.archivo_path, mode='a', newline='', encoding='utf-8') as file:
            #En este caso usamos el modo 'a' para abrir el archivo usando el modo append, lo que significa que los nuevos registros se agregarán al final del archivo sin sobrescribir los datos existentes. 
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(registro_dict)

    #metodo para poder guardar todo el diccionario de 0
    def guardar_todo(self, lista_registros):
        with open(self.archivo_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader() #Escribimos el encabezado antes de escribir los registros
            writer.writerows(lista_registros) #Escribimos todos los registros de la lista en el archivo CSV

    #metodo para obtener el ultimo id nuevo que se hara
    def obtener_nuevo_id(self):
        registros = self.leer_todos()
        if not registros:
            return 1
        nombre_columna_id = self.fieldnames[0] #Asumimos que el primer campo es el ID
        ultimo_registro = registros[-1]

        return int(ultimo_registro[nombre_columna_id]) + 1