from infrastructure.file_manager import FileManager
from datetime import datetime

class ClientService:
    def __init__(self):
        self.db_cuentas = FileManager('cuentas.csv', ['id_cuenta', 'propietario_id', 'tipo', 'saldo', 'estado'])
        self.db_transacciones = FileManager('transacciones.csv', ['id_transaccion', 'id_cuenta', 'tipo_movimiento', 'monto', 'fecha'])
        self.db_transferencias = FileManager('transferencias.csv', ['id_transferencia', 'cuenta_origen', 'cuenta_destino', 'monto', 'fecha'])

    def obtener_mis_cuentas(self, propietario_id):
        #Devuelve solo las cuentas del cliente logueado
        todas = self.db_cuentas.leer_todos()
        return [c for c in todas if str(c['propietario_id']) == str(propietario_id)]

    def procesar_transaccion(self, id_cuenta, tipo_movimiento, monto):
        #Maneja tanto depósitos como retiros aplicando las reglas de negocio
        monto = float(monto)
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a $0.00") # Regla: monto > 0
            
        todas_cuentas = self.db_cuentas.leer_todos()
        cuenta_encontrada = None
        
        # 1. Buscar la cuenta y validar
        for cuenta in todas_cuentas:
            if str(cuenta['id_cuenta']) == str(id_cuenta):
                if cuenta['estado'] != 'Activa':
                    raise ValueError("La cuenta está bloqueada y no acepta transacciones.") # Regla: cuenta activa
                cuenta_encontrada = cuenta
                break
                
        if not cuenta_encontrada:
            raise ValueError("La cuenta no existe.")

        saldo_actual = float(cuenta_encontrada['saldo'])

        # 2. Lógica matemática
        if tipo_movimiento == "RETIRO":
            if saldo_actual < monto:
                raise ValueError("Fondos insuficientes para realizar el retiro.") # Regla: saldo suficiente
            cuenta_encontrada['saldo'] = saldo_actual - monto
        elif tipo_movimiento == "DEPOSITO":
            cuenta_encontrada['saldo'] = saldo_actual + monto

        # 3. Guardar el nuevo saldo en cuentas.csv
        self.db_cuentas.guardar_todo(todas_cuentas)

        # 4. Registrar en el historial transacciones.csv con fecha/hora
        nuevo_id_transaccion = self.db_transacciones.obtener_nuevo_id()
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Regla: registrar fecha/hora
        
        nueva_transaccion = {
            'id_transaccion': nuevo_id_transaccion,
            'id_cuenta': id_cuenta,
            'tipo_movimiento': tipo_movimiento,
            'monto': monto,
            'fecha': fecha_hora
        }
        self.db_transacciones.agregar(nueva_transaccion)
        
        return cuenta_encontrada['saldo'] # Devolvemos cómo quedó el saldo
    
    def transferir(self, id_cuenta_origen, id_cuenta_destino, monto):
        #Mueve dinero entre cuentas y genera registros para analítica
        monto = float(monto)
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a $0.00")
            
        if str(id_cuenta_origen) == str(id_cuenta_destino):
            raise ValueError("No puedes transferir dinero a la misma cuenta.")

        todas_cuentas = self.db_cuentas.leer_todos()
        cuenta_origen = None
        cuenta_destino = None

        #Buscar ambas cuentas
        for cuenta in todas_cuentas:
            if str(cuenta['id_cuenta']) == str(id_cuenta_origen):
                cuenta_origen = cuenta
            if str(cuenta['id_cuenta']) == str(id_cuenta_destino):
                cuenta_destino = cuenta

        #Validaciones 
        if not cuenta_origen:
            raise ValueError("Tu cuenta de origen no existe.")
        if cuenta_origen['estado'] != 'Activa':
            raise ValueError("Tu cuenta de origen está bloqueada.")
            
        if not cuenta_destino:
            raise ValueError("La cuenta de destino no existe. (Operación abortada)")
        if cuenta_destino['estado'] != 'Activa':
            raise ValueError("La cuenta de destino está bloqueada por el administrador.")
            
        if float(cuenta_origen['saldo']) < monto:
            raise ValueError("Fondos insuficientes para esta transferencia.")

        
        cuenta_origen['saldo'] = float(cuenta_origen['saldo']) - monto
        cuenta_destino['saldo'] = float(cuenta_destino['saldo']) + monto

        
        self.db_cuentas.guardar_todo(todas_cuentas)

        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Registrar movimientos individuales en el historial (Para el cliente)
        self.db_transacciones.agregar({
            'id_transaccion': self.db_transacciones.obtener_nuevo_id(),
            'id_cuenta': id_cuenta_origen,
            'tipo_movimiento': 'TRANSFER_OUT',
            'monto': monto,
            'fecha': fecha_hora
        })
        self.db_transacciones.agregar({
            'id_transaccion': self.db_transacciones.obtener_nuevo_id(),
            'id_cuenta': id_cuenta_destino,
            'tipo_movimiento': 'TRANSFER_IN',
            'monto': monto,
            'fecha': fecha_hora
        })

        #Registrar en el archivo exclusivo de transferencias 
        self.db_transferencias.agregar({
            'id_transferencia': self.db_transferencias.obtener_nuevo_id(),
            'cuenta_origen': id_cuenta_origen,
            'cuenta_destino': id_cuenta_destino,
            'monto': monto,
            'fecha': fecha_hora
        })
        
        return float(cuenta_origen['saldo'])

    def obtener_historial_movimientos(self, propietario_id):
        """Busca todas las transacciones de todas las cuentas de un cliente"""
        mis_cuentas = self.obtener_mis_cuentas(propietario_id)
        # Extraemos solo los IDs de mis cuentas para filtrar rápido
        mis_ids_cuentas = [str(c['id_cuenta']) for c in mis_cuentas] 
        
        todas_transacciones = self.db_transacciones.leer_todos()
        
        mi_historial = []
        for t in todas_transacciones:
            if str(t['id_cuenta']) in mis_ids_cuentas:
                mi_historial.append(t)
                
        return mi_historial