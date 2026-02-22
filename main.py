import os
import time
from application.auth_service import AuthService

# Instanciamos el servicio
auth_service = AuthService()

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
        # menu_admin(usuario) <-- PRÓXIMO PASO
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

if __name__ == "__main__":
    menu_principal()