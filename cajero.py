usuario_guardado = "joaquin" # valores de prueba, deberia recibir la información desde la base de datos 
contraseña_guardada = "1234" # valores de prueba, deberia recibir la información desde la base de datos 
saldo_guardado = 100 # valores de prueba, deberia recibir la información desde la base de datos 


def opciones():
    
    try:
        opcion = int(input("""A continuación, seleccione la operación que desea realizar
            1 - Consultar saldo
            2 - Retirar saldo
            3 - Transferir
            4 - Salir
        """))
        return opcion
    
    except ValueError:
        print('Seleccione una opción válida')
        return None
        
def consultar_saldo(saldo):
    print(f'Su saldo disponible es de: {saldo}')

def retirar_saldo(saldo):
    
    try:
        cantidad = int(input("Ingrese la cantidad a retirar: "))
        if cantidad > saldo:
            print('Saldo no disponible')
        else:
            print('Saldo retirado con éxito')
            saldo -= cantidad
    except ValueError:
        print('Ingrese un número válido')
        
    return saldo

def transferir_saldo(saldo):
    
    try:
        cantidad = int(input("Ingrese la cantidad a transferir: "))
        if cantidad > saldo:
            print('Saldo no disponible')
        else:
            print('Saldo transferido con éxito')
            saldo -= cantidad
    except ValueError:
        print('Ingrese un número válido')
        
    return saldo

def terminar_programa():
    print('Saliendo del sistema')

def iniciar_cajero():
    
    saldo = saldo_guardado

    intentos = 3

    while intentos > 0:
        usuario = input('Ingrese su nombre de usuario: ')
        contraseña = input('Ingrese su contraseña: ')

        if usuario.lower() == usuario_guardado.lower() and contraseña == contraseña_guardada:
            print(f'Bienvenido {usuario}')
            
            while True:
                opcion = opciones()
                if opcion == 1:
                    consultar_saldo(saldo)
                elif opcion == 2:
                    saldo = retirar_saldo(saldo)
                elif opcion == 3:
                    saldo = transferir_saldo(saldo)
                elif opcion == 4:
                    terminar_programa()
                    return
                else:
                    print('Opción inválida. Intente de nuevo.')
        else:
            intentos -= 1
            print(f'Usuario o contraseña incorrectos. Intentos restantes: {intentos}')
            if intentos == 0:
                print('Demasiados intentos. Reinicie el programa e intente de nuevo.')
                break


iniciar_cajero()