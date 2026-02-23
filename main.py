



import os
import time
from application.auth_service import AuthService
from application.admin_service import AdminService

# Instanciamos el servicio
auth_service = AuthService()
admin_service = AdminService()

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
    username = input("Username (Ej. KL1): ").strip() .upper()
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
        # menu_cliente(usuario) <-- PRÓXIMO PASO
    else:
        print("\n❌ Credenciales incorrectas o no eres Cliente.")
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
            from application.analytics_service import AnalyticsService
            analytics = AnalyticsService()
            analytics.estadisticas_por_cuenta()
            input("\nPresione Enter para continuar ....")
        #Aca ira la parte de analisis de datos, que se hara al final del proyecto, por ahora solo es un placeholder
        elif opcion == '6':
            return
        else:
            print("Opción inválida.")
            time.sleep(1)

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