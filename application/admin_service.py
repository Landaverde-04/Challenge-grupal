from infrastructure.file_manager import FileManager
from domain.models import Usuario, Cuenta

class AdminService:
    def __init__(self):
        self.db_usuarios = FileManager('usuarios.csv', ['id', 'nombres', 'apellidos', 'dui', 'pin', 'rol', 'username'])
        self.db_cuentas = FileManager('cuentas.csv', ['id_cuenta', 'propietario_id', 'tipo', 'saldo', 'estado'])

    def crear_cliente(self, nombres, apellidos, dui, pin):
        nuevo_id = self.db_usuarios.obtener_nuevo_id()
        nuevo_cliente = Usuario(nuevo_id, nombres, apellidos, dui, pin, "Cliente", "")        
        self.db_usuarios.agregar(nuevo_cliente.to_dict())
        return nuevo_cliente
    
    def crear_cuenta(self, propietario_id, tipo):
        #Crea una cuenta bancaria inicializada en $0.0 y Activa
        nuevo_id_cuenta = self.db_cuentas.obtener_nuevo_id()
        nueva_cuenta = Cuenta(nuevo_id_cuenta, propietario_id, tipo, 0.0, "Activa")
        self.db_cuentas.agregar(nueva_cuenta.to_dict())
        return nueva_cuenta
        
    def listar_clientes(self):
        #Lee todos los usuarios del archivo CSV y filtra solo aquellos que tienen el rol de "Cliente"
        todos = self.db_usuarios.leer_todos()
        return [u for u in todos if u['rol'] == 'Cliente']
    
    def obtener_cuentas_cliente(self, propietario_id):
        #Lee todas las cuentas del archivo CSV y filtra solo aquellas que pertenecen al cliente con el ID proporcionado
        todas = self.db_cuentas.leer_todos()
        cuentas_del_cliente = []
        for c in todas:
            if c['propietario_id'] == propietario_id:
                cuentas_del_cliente.append(c)

        return cuentas_del_cliente
    
    def cambiar_estado_cuenta(self, id_cuenta):
        todas = self.db_cuentas.leer_todos()
        encontrada = False
        nuevo_estado = ""
        for c in todas:
            if str(c['id_cuenta']) == str(id_cuenta):
                encontrada = True
                if c['estado'] == "Activa":
                    c['estado'] = "Bloqueada"                    
                else:
                    c['estado'] = "Activa"
                nuevo_estado = c['estado']
                break
        if encontrada:
            self.db_cuentas.guardar_todo(todas)
            return True, nuevo_estado
        return False, ""