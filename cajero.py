import sqlite3

# datos:
# usuario: joaquin
# contraseña: 1234
# saldo incial: 1000 

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
    try:
        
        conexion = sqlite3.connect('cajero.db')
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                contraseña TEXT NOT NULL,
                saldo REAL DEFAULT 0
            )
        ''')
        
        cursor.execute('SELECT COUNT(*) FROM usuarios')
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                'INSERT INTO usuarios (nombre, contraseña, saldo) VALUES (?,?,?)',
                ('joaquin', '1234', 1000.0)
            )
            conexion.commit()

        intentos = 3

        while intentos > 0:
            usuario = input('Ingrese su nombre de usuario: ')
            contraseña = str(input('Ingrese su contraseña: '))

            
            cursor.execute('SELECT id, saldo FROM usuarios WHERE nombre = ? AND contraseña = ?', (usuario, contraseña))
            resultado = cursor.fetchone()

            if resultado:
                id_usuario, saldo = resultado
                print(f'Bienvenido {usuario}')

                while True:
                    opcion = opciones()
                    if opcion == 1:
                        consultar_saldo(saldo)
                    elif opcion == 2:
                        saldo = retirar_saldo(saldo)
                        # 3. Actualizar el saldo en la base
                        cursor.execute('UPDATE usuarios SET saldo = ? WHERE id = ?', (saldo, id_usuario))
                        conexion.commit()
                    elif opcion == 3:
                        saldo = transferir_saldo(saldo)
                        cursor.execute('UPDATE usuarios SET saldo = ? WHERE id = ?', (saldo, id_usuario))
                        conexion.commit()
                    elif opcion == 4:
                        terminar_programa()
                        conexion.close()
                        return
                    else:
                        print('Opción inválida. Intente de nuevo.')
            else:
                intentos -= 1
                print(f'Usuario o contraseña incorrectos. Intentos restantes: {intentos}')
                if intentos == 0:
                    print('Demasiados intentos. Reinicie el programa e intente de nuevo.')
                    conexion.close()
                    break
    finally:
        try:
            conexion.close()
        except NameError:
            pass

iniciar_cajero()