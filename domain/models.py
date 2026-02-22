from datetime import datetime

class Usuario:
    def __init__(self, id, nombres, apellidos, dui, pin, rol, username=None):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.dui = dui
        self.pin = pin
        self.rol = rol
        
        if self.rol == 'Administrador':
            if username:
                self.username = username
            else:
                self.username = self._generar_username_admin()

        else:
            self.username = ""

    def _generar_username_admin(self):
        primer_nombre = self.nombres.split()[0] 
        primer_apellido = self.apellidos.split()[0]
        siglas = primer_nombre[0] + primer_apellido[0]
        return f"{siglas.upper()}{self.id}"
        
    def to_dict(self):
        return {
                'id': self.id,
                'nombres': self.nombres,
                'apellidos': self.apellidos,
                'dui': self.dui,
                'pin': self.pin,
                'rol': self.rol,
                'username': self.username
            }
    
class Cuenta:
    def __init__(self, id_cuenta, propietario_id, tipo, saldo=0.0, estado="Activa"):
        self.id_cuenta = id_cuenta
        self.propietario_id = propietario_id # Relación con el ID del Usuario [cite: 163]
        self.tipo = tipo # "Ahorro" o "Corriente" 
        self.saldo = float(saldo)
        self.estado = estado # "Activa" o "Bloqueada" 

    def to_dict(self):
        return {
            'id_cuenta': self.id_cuenta,
            'propietario_id': self.propietario_id,
            'tipo': self.tipo,
            'saldo': self.saldo,
            'estado': self.estado
        }

