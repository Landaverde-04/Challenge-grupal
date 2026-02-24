import os
import time
from application.auth_service import AuthService
from application.admin_service import AdminService

# Instanciamos servicios
auth_service = AuthService()
admin_service = AdminService()


# -------------------------------------------------
# MENÚ PRINCIPAL
# -------------------------------------------------
def menu_principal():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== SISTEMA BANCARIO ===")
        print("1. Ingresar como Administrador")
        print("2. Ingresar como Cliente")
        print("3. Salir del sistema")

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


# -------------------------------------------------
# LOGIN ADMIN
# -------------------------------------------------
def login_admin_view():
    os.system("cls" if os.name == "nt" else "clear")
    print("--- LOGIN ADMINISTRADOR ---")
    username = input("Username (Ej. KL1): ").strip().upper()
    pin = input("PIN: ").strip()

    usuario = auth_service.login_admin(username, pin)

    if usuario:
        print(f"\nBienvenido, Admin {usuario.nombres}!")
        time.sleep(1)
        menu_admin(usuario)
    else:
        print("\nCredenciales incorrectas o no eres Administrador.")
        time.sleep(2)


# -------------------------------------------------
# LOGIN CLIENTE
# -------------------------------------------------
def login_cliente_view():
    os.system("cls" if os.name == "nt" else "clear")
    print("--- LOGIN CLIENTE ---")
    dui = input("DUI (Ej. 12345678-9): ").strip()
    pin = input("PIN: ").strip()

    usuario = auth_service.login_cliente(dui, pin)

    if usuario:
        print(f"\nBienvenido, Cliente {usuario.nombres}!")
        time.sleep(1)
        # Aquí irá menú cliente
    else:
        print("\nCredenciales incorrectas o no eres Cliente.")
        time.sleep(2)


# -------------------------------------------------
# MENÚ ADMINISTRADOR
# -------------------------------------------------
def menu_admin(admin_actual):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"--- MENÚ ADMINISTRADOR ({admin_actual.nombres}) ---")
        print("1. Crear nuevo cliente")
        print("2. Crear cuenta para cliente")
        print("3. Bloquear/Desbloquear cuenta")
        print("4. Listar usuarios y cuentas")
        print("5. Módulo de análisis")
        print("6. Salir de cuenta de ADMINISTRADOR")

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
            menu_analisis()
        elif opcion == '6':
            return
        else:
            print("Opción inválida.")
            time.sleep(1)


# -------------------------------------------------
# SUBMENÚ ANÁLISIS
# -------------------------------------------------
def menu_analisis():
    from application.analytics_service import AnalyticsService

    analytics = AnalyticsService()

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== MÓDULO DE ANÁLISIS ===")
        print("1. Estadísticas por cuenta")
        print("2. Dashboard administrador")
        print("3. Anomalías")
        print("4. Serie temporal neto")
        print("5. Heatmap actividad")
        print("6. boxplot montos")
        print("7. Depósito versus gastos")
        print("8. Grafico transferencias")
        print("9. Volver al menu anterior")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            analytics.estadisticas_por_cuenta()
            input("\nPresione Enter para continuar...")
        elif opcion == '2':
            analytics.dashboard_admin()
            input("\nPresione Enter para continuar...")
        elif opcion == '3':
            analytics.detectar_anomalias()
            input("\nPresione Enter para continuar...")
        elif opcion == '4':
            analytics.plot_serie_temporal_neto()
            input("\nPresione Enter para continuar ..")
        elif opcion == '5':
            analytics.plot_heatmap_actividad()
            input("\nPresione Enter para continuar ..")
        elif opcion == '6':
            analytics.plot_boxplot_montos()
            input("\nPresione Enter para continuar ..")
        elif opcion == '7':
            analytics.plot_scatter_depositos_vs_gastos()
            input("\nPresione enter para continuar...")
        elif opcion == '8':
            analytics.plot_grafo_flujo_financiero()
            input("\nPresiona Enter para continuar ..")
        elif opcion == '9':
            break
        else:
            print("opcion inválida")
            time.sllep(1)
        

# CREAR CLIENTE

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


# -------------------------------------------------
# CREAR CUENTA
# -------------------------------------------------
def crear_cuenta_view():
    os.system("cls" if os.name == "nt" else "clear")
    print("--- CREAR CUENTA PARA CLIENTE ---")

    listar_usuarios_cuentas_view()
    propietario_id = input("ID del propietario (Cliente): ").strip()

    if not propietario_id:
        print("Error: El ID del propietario es obligatorio.")
        input("\nPresione Enter para continuar...")
        return

    cuentas_existentes = admin_service.obtener_cuentas_cliente(propietario_id)

    print("Tipos de cuenta disponibles: 1. Ahorro, 2. Corriente")
    opc_tipo = input("Seleccione el tipo de cuenta (1 o 2): ").strip()
    tipo = "Ahorro" if opc_tipo == '1' else "Corriente"

    for cuenta in cuentas_existentes:
        if cuenta['tipo'] == tipo:
            print(f"Error: El cliente ya tiene una cuenta de tipo {tipo}.")
            input("\nPresione Enter para continuar...")
            return

    cuenta = admin_service.crear_cuenta(propietario_id, tipo)

    print(f"\nCuenta de {cuenta.tipo} creada con éxito.")
    print(f"Número de cuenta asignado: {cuenta.id_cuenta}")

    input("\nPresione Enter para continuar...")


# LISTAR USUARIOS
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
                    print(f"     - N°: {cuenta['id_cuenta']} | Tipo: {cuenta['tipo']} | "
                          f"Saldo: ${float(cuenta['saldo']):.2f} | Estado: {cuenta['estado']}")
            else:
                print("   ↳ (Sin cuentas asignadas)")

    input("\nPresione Enter para continuar...")


# BLOQUEAR/DESBLOQUEAR
def vista_cambiar_estado_cuenta():
    os.system("cls" if os.name == "nt" else "clear")
    print("--- BLOQUEAR/DESBLOQUEAR CUENTA ---")

    listar_usuarios_cuentas_view()
    propietario_id = input("Ingrese el ID del cliente: ").strip()

    if not propietario_id:
        print("Error: El ID es obligatorio.")
        input("\nPresione Enter para continuar...")
        return

    cuentas = admin_service.obtener_cuentas_cliente(propietario_id)

    if not cuentas:
        print("No se encontraron cuentas.")
        input("\nPresione Enter para continuar...")
        return

    for c in cuentas:
        print(f"ID Cuenta: {c['id_cuenta']} | Tipo: {c['tipo']} | Estado actual: {c['estado']}")

    id_cuenta = input("Ingrese el ID de la cuenta: ").strip()

    exito, nuevo_estado = admin_service.cambiar_estado_cuenta(id_cuenta)

    if exito:
        print(f"\nCuenta {id_cuenta} ahora está {nuevo_estado}.")
    else:
        print("Cuenta no encontrada.")

    input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()