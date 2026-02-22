from infrastructure.file_manager import FileManager
from domain.models import Usuario

class AuthService:
    def __init__(self):
        self.columnas = ['id', 'nombres', 'apellidos', 'dui', 'pin', 'rol', 'username']
        self.db = FileManager('usuarios.csv', self.columnas)

    def login_admin(self, username, pin):
        usuarios = self.db.leer_todos()
        
        for u_data in usuarios:
            if u_data['rol'] == 'Administrador' and u_data['username'] == username and u_data['pin'] == pin:                
                return Usuario(
                    id=u_data['id'],
                    nombres=u_data['nombres'],
                    apellidos=u_data['apellidos'],
                    dui=u_data['dui'],
                    pin=u_data['pin'],
                    rol=u_data['rol'],
                    username=u_data['username']
                )
        return None # Credenciales incorrectas
    
    def login_cliente(self, dui, pin):
        usuarios = self.db.leer_todos()
        
        for u_data in usuarios:
            if u_data['rol'] == 'Cliente' and u_data['dui'] == dui and u_data['pin'] == pin:                
                return Usuario(
                    id=u_data['id'],
                    nombres=u_data['nombres'],
                    apellidos=u_data['apellidos'],
                    dui=u_data['dui'],
                    pin=u_data['pin'],
                    rol=u_data['rol'],
                    username=""
                )
        return None # Credenciales incorrectas