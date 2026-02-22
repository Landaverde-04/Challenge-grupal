import os
import time
from application.auth_service import AuthService
from application.admin_service import AdminService
from application.client_service import ClientService

# Instanciamos el servicio
auth_service = AuthService()
admin_service = AdminService()
client_service = ClientService()

def menu_principal():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== SISTEMA BANCARIO ===")
        print("1. Ingresar como Administrador")
        print("2. Ingresar como Cliente")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            login_admin_view()
        elif opcion == '2':
            login_cliente_view()
        elif opcion == '3':
            print("Saliendo del sistema...")
            time.sleep(1)
            break
        else:
            print("Opción inválida.")
            time.sleep(1)

def login_admin_view():
    os.system("cls" if os.name == "nt" else "clear")
    print("--- LOGIN ADMINISTRADOR ---")
    username = input("Username (Ej. KL1): ").strip()
    pin = input("PIN: ").strip()
    
    usuario = auth_service.login_admin(username, pin)
    
    if usuario:
        print(f"\nBienvenido, Admin {usuario.nombres}!")
        time.sleep(1)
        menu_admin(usuario)
    else:
        print("\nCredenciales incorrectas o no eres Administrador.")
        time.sleep(2)

def login_cliente_view():
    os.system("cls" if os.name == "nt" else "clear")
    print("--- LOGIN CLIENTE ---")
    dui = input("DUI (Ej. 12345678-9): ").strip()
    pin = input("PIN: ").strip()
    
    usuario = auth_service.login_cliente(dui, pin)
    
    if usuario:
        print(f"\nBienvenido, Cliente {usuario.nombres}!")
        time.sleep(1)
        menu_cliente(usuario) 
    else:
        print("\nCredenciales incorrectas o no eres Cliente.")
        time.sleep(2)

def menu_admin(admin_actual):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"--- MENÚ ADMINISTRADOR ({admin_actual.nombres}) ---")
        print("1. Crear nuevo cliente")
        print("2. Crear cuenta para cliente")
        print("3. Bloquear/Desbloquear cuenta")
        print("4. Listar usuarios y cuentas")
        print("5. Modulo de analisis")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            crear_cliente_view()
        elif opcion == '2':
            crear_cuenta_view()
        elif opcion == '3':
            vista_cambiar_estado_cuenta()
        elif opcion == '4':
            listar_usuarios_cuentas_view()
        elif opcion == '5':
            pass
        #Aca ira la parte de analisis de datos, que se hara al final del proyecto, por ahora solo es un placeholder
        elif opcion == '6':
            return
        else:
            print("Opción inválida.")
            time.sleep(1)

def menu_cliente(cliente_actual):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"--- MENÚ CLIENTE: {cliente_actual.nombres} {cliente_actual.apellidos} ---")
        print("1. Ver saldo de mis cuentas")
        print("2. Depositar")
        print("3. Retirar")
        print("4. Ver historial de movimientos ")
        print("5. Transferir a terceros ")
        print("6. Cerrar sesión")
        
        opcion = input("Opción: ")
        
        if opcion == '1':
            vista_ver_saldos(cliente_actual)
        elif opcion == '2':
            vista_transaccion(cliente_actual, "DEPOSITO")
        elif opcion == '3':
            vista_transaccion(cliente_actual, "RETIRO")
        elif opcion == '4':
            vista_historial(cliente_actual)
        elif opcion == '5':
            vista_transferir(cliente_actual)
        elif opcion == '6':
            return
        else:
            print("Opción no válida.")
            time.sleep(1)

def vista_transferir(cliente_actual):
    os.system("cls" if os.name == "nt" else "clear")
    print("--- TRANSFERENCIAS ---")
    
    # Mostramos las cuentas disponibles del cliente
    cuentas = client_service.obtener_mis_cuentas(cliente_actual.id)
    if not cuentas:
        print("No tienes cuentas para realizar transferencias.")
        time.sleep(2); return
        
    print("Tus cuentas disponibles para origen:")
    for c in cuentas:
        print(f"- N°: {c['id_cuenta']} | {c['tipo']} | Saldo: ${float(c['saldo']):.2f}")
        
    id_origen = input("\nIngrese su N° de cuenta origen: ").strip()
    id_destino = input("Ingrese el N° de cuenta destino (Propia o Tercero): ").strip()
    monto_str = input("Ingrese el monto a transferir: $").strip()
    
    try:
        nuevo_saldo = client_service.transferir(id_origen, id_destino, monto_str)
        print("\nTransferencia enviada con éxito.")
        print(f"Saldo restante en tu cuenta origen: ${nuevo_saldo:.2f}")
    except ValueError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nError inesperado. Verifique los datos ingresados: {e}")
        
    input("\nPresione Enter para continuar...")

def vista_historial(cliente_actual):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"--- HISTORIAL DE MOVIMIENTOS ---")
    
    historial = client_service.obtener_historial_movimientos(cliente_actual.id)
    
    if not historial:
        print("No tienes movimientos registrados aún.")
    else:
        print(f"{'FECHA':<20} | {'CUENTA':<10} | {'MOVIMIENTO':<15} | {'MONTO'}")
        print("-" * 60)
        # Mostrar el historial al revés (los más recientes primero)
        for t in reversed(historial):
            # Formateamos visualmente para que se entienda mejor
            simbolo = "+" if t['tipo_movimiento'] in ['DEPOSITO', 'TRANSFER_IN'] else "-"
            print(f"{t['fecha']:<20} | {t['id_cuenta']:<10} | {t['tipo_movimiento']:<15} | {simbolo}${float(t['monto']):.2f}")
            
    input("\nPresione Enter para volver...")

def vista_ver_saldos(cliente_actual):
    os.system("cls" if os.name == "nt" else "clear")
    print("--- MIS CUENTAS Y SALDOS ---")
    
    cuentas = client_service.obtener_mis_cuentas(cliente_actual.id)
    if not cuentas:
        print("Aún no tienes cuentas abiertas en nuestro banco.")
    else:
        print(f"{'N° CUENTA':<10} | {'TIPO':<10} | {'SALDO':<10} | {'ESTADO'}")
        print("-" * 50)
        for c in cuentas:
            print(f"{c['id_cuenta']:<10} | {c['tipo']:<10} | ${float(c['saldo']):<9.2f} | {c['estado']}")
            
    input("\nPresione Enter para volver...")

def vista_transaccion(cliente_actual, tipo_movimiento):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"--- NUEVO {tipo_movimiento} ---")
    
    # Mostrar sus cuentas para que sepa los IDs
    cuentas = client_service.obtener_mis_cuentas(cliente_actual.id)
    if not cuentas:
        print("No tienes cuentas para realizar esta operación.")
        time.sleep(2); return
        
    for c in cuentas:
        print(f"Cuenta: {c['id_cuenta']} | {c['tipo']} | Saldo: ${float(c['saldo']):.2f} | Estado: {c['estado']}")
        
    id_cuenta = input("\nIngrese el N° de cuenta a utilizar: ").strip()
    monto_str = input(f"Ingrese el monto a {tipo_movimiento.lower()}: $").strip()
    
    try:
        # Llamamos al servicio para que aplique las reglas de negocio
        nuevo_saldo = client_service.procesar_transaccion(id_cuenta, tipo_movimiento, monto_str)
        print(f"\n{tipo_movimiento.capitalize()} exitoso.")
        print(f"Tu nuevo saldo es: ${nuevo_saldo:.2f}")
    except ValueError as e:
        # Si el servicio detecta un error (saldo insuficiente, monto negativo), lo mostramos aquí
        print(f"\nError: {e}")
    except Exception as e:
        print("\nError inesperado. Ingrese un monto numérico válido.")
        
    input("\nPresione Enter para continuar...")

def crear_cliente_view():
    os.system("cls" if os.name == "nt" else "clear")
    print("--- CREAR NUEVO CLIENTE ---")
    nombres = input("Nombres: ").strip()
    apellidos = input("Apellidos: ").strip()
    dui = input("DUI (Ej. 12345678-9): ").strip()
    pin = input("PIN de 4 digitos: ").strip()
    
    if nombres and apellidos and dui and pin:
        nuevo_cliente = admin_service.crear_cliente(nombres, apellidos, dui, pin)
        print(f"\nCliente creado con éxito! Nombre: {nuevo_cliente.nombres}")
    else:
        print("Error: Todos los campos son obligatorios.")

    input("\nPresione Enter para continuar...")

def crear_cuenta_view():
    os.system("cls" if os.name == "nt" else "clear")
    print("--- CREAR CUENTA PARA CLIENTE ---")
    listar_usuarios_cuentas_view() # Mostramos la lista de clientes para que el admin pueda elegir el ID del propietario
    propietario_id = input("ID del propietario (Cliente): ").strip()
    if not propietario_id:
        print("Error: El ID del propietario es obligatorio.")
        input("\nPresione Enter para continuar...")
        return
    cuentas_existentes = admin_service.obtener_cuentas_cliente(propietario_id)
    if cuentas_existentes:
        print("\nCuentas actuales del cliente:")
        print(f"{'N° CUENTA':<10} | {'TIPO':<10} | {'ESTADO':<10}")
        print("-" * 35)
        for c in cuentas_existentes:
            print(f"{c['id_cuenta']:<10} | {c['tipo']:<10} | {c['estado']:<10}")
        print("-" * 35)
    else:
        print("\nEl cliente es nuevo, no tiene cuentas registradas.")
    print("Tipos de cuenta disponibles: 1. Ahorro, 2. Corriente")
    opc_tipo = input("Seleccione el tipo de cuenta (1 o 2): ").strip()
    tipo = "Ahorro" if opc_tipo == '1' else "Corriente"
    
    cuentas_existentes = admin_service.obtener_cuentas_cliente(propietario_id)

    for cuentas in cuentas_existentes:
        if cuentas['tipo'] == tipo:
            print(f"Error: El cliente ya tiene una cuenta de tipo {tipo}.")
            input("\nPresione Enter para continuar...")
            return

    cuenta = admin_service.crear_cuenta(propietario_id, tipo)
    print(f"\nCuenta de {cuenta.tipo} creada con éxito.")
    print(f"Numero de cuenta asignado: {cuenta.id_cuenta}")

    input("\nPresione Enter para continuar...")

def listar_usuarios_cuentas_view():
    print("--- LISTA DE CLIENTES ---")
    clientes = admin_service.listar_clientes()
    if not clientes:
        print("No hay clientes registrados.")
    else:
        print(f"{'ID':<5} | {'NOMBRES':<20} | {'DUI':<12}")
        print("-" * 45)
        for c in clientes:
            print(f"{c['id']:<5} | {c['nombres'] + ' ' + c['apellidos']:<20} | {c['dui']:<12}")
            cuentas = admin_service.obtener_cuentas_cliente(c['id'])
            if cuentas:
                print("   ↳ Cuentas:")
                for cuenta in cuentas:
                    print(f"     - N°: {cuenta['id_cuenta']} | Tipo: {cuenta['tipo']} | Saldo: ${float(cuenta['saldo']):.2f} | Estado: {cuenta['estado']}")
            else:
                print("   ↳ (Sin cuentas asignadas)")        
    input("\nPresione Enter para continuar...")

def vista_cambiar_estado_cuenta():
    os.system("cls" if os.name == "nt" else "clear")
    print("--- BLOQUEAR/DESBLOQUEAR CUENTA ---")
    listar_usuarios_cuentas_view() # Mostramos la lista de clientes para que el admin pueda elegir el ID del propietario
    propietario_id = input("Ingrese el ID del cliente para ver sus cuentas: ").strip()
    if not propietario_id:
        print("Error: El ID del cliente es obligatorio.")
        input("\nPresione Enter para continuar...")
        return
    cuentas = admin_service.obtener_cuentas_cliente(propietario_id)
    if not cuentas:
        print(f"No se encontraron cuentas para el ID de cliente {propietario_id}.")
        input("\nPresione Enter para continuar...")
        return
    print("\nCuentas encontradas:")
    for c in cuentas:
        print(f"ID Cuenta: {c['id_cuenta']} | Tipo: {c['tipo']} | Estado actual: {c['estado']}")
    

    id_cuenta = input("Ingrese el ID de la cuenta a bloquear/desbloquear: ").strip()
    if not id_cuenta:
        print("Error: El ID de la cuenta es obligatorio.")
        input("\nPresione Enter para continuar...")
        return

    exito, nuevo_estado = admin_service.cambiar_estado_cuenta(id_cuenta)
    if exito:
        print(f"\nCuenta {id_cuenta} ahora está {nuevo_estado}.")
    else:
        print(f"\nError: No se encontró la cuenta con ID {id_cuenta}.")

    input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()