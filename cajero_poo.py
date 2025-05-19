import sqlite3
import time

class BaseDeDatos:
    def __init__(self, db_name='cajero.db'):
        self.db_name = db_name
        self.conexion = None
        self.cursor = None
    
    def conectar(self):
        self.conexion = sqlite3.connect(self.db_name)
        self.cursor = self.conexion.cursor()
    
    def crear_tabla_usuarios(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                contraseña TEXT NOT NULL,
                saldo REAL DEFAULT 0
            )
        ''')
    
    def verificar_usuarios_existentes(self):
        self.cursor.execute('SELECT COUNT(*) FROM usuarios')
        return self.cursor.fetchone()[0]
    
    def usuario_existe(self, nombre_usuario):
        """Verifica si un usuario ya existe en la base de datos"""
        self.cursor.execute('SELECT COUNT(*) FROM usuarios WHERE nombre = ?', (nombre_usuario,))
        return self.cursor.fetchone()[0] > 0
    
    def crear_nuevo_usuario(self, nombre, contraseña, saldo_inicial=0.0):
        """Crea un nuevo usuario en la base de datos"""
        self.cursor.execute(
            'INSERT INTO usuarios (nombre, contraseña, saldo) VALUES (?,?,?)',
            (nombre, contraseña, saldo_inicial)
        )
        self.conexion.commit()
    
    def crear_usuario_inicial(self):
        self.cursor.execute(
            'INSERT INTO usuarios (nombre, contraseña, saldo) VALUES (?,?,?)',
            ('joaquin', '1234', 1000.0)
        )
        self.conexion.commit()
    
    def autenticar_usuario(self, usuario, contraseña):
        self.cursor.execute('SELECT id, saldo FROM usuarios WHERE nombre = ? AND contraseña = ?', 
                           (usuario, contraseña))
        return self.cursor.fetchone()
    
    def actualizar_saldo(self, id_usuario, nuevo_saldo):
        self.cursor.execute('UPDATE usuarios SET saldo = ? WHERE id = ?', (nuevo_saldo, id_usuario))
        self.conexion.commit()
    
    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()
    
    def obtener_usuarios(self):
        """Obtiene la lista de todos los usuarios registrados"""
        self.cursor.execute('SELECT nombre FROM usuarios ORDER BY nombre')
        return [row[0] for row in self.cursor.fetchall()]


class Usuario:
    def __init__(self, id_usuario, nombre, saldo, db):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.saldo = saldo
        self.db = db
    
    def consultar_saldo(self):
        imprimir_con_delay(f'Su saldo disponible es de: {self.saldo}')
    
    def retirar_saldo(self):
        try:
            cantidad = int(input("Ingrese la cantidad a retirar: "))
            if cantidad > self.saldo:
                imprimir_con_delay('Saldo no disponible')
            else:
                imprimir_con_delay('Saldo retirado con éxito')
                self.saldo -= cantidad
                self.db.actualizar_saldo(self.id_usuario, self.saldo)
        except ValueError:
            imprimir_con_delay('Ingrese un número válido')
        
        return self.saldo
    
    def depositar_saldo(self):
        try:
            cantidad = int(input("Ingrese la cantidad a depositar: "))
            if cantidad <= 0:
                imprimir_con_delay('Por favor ingrese una cantidad válida mayor a cero')
            else:
                self.saldo += cantidad
                self.db.actualizar_saldo(self.id_usuario, self.saldo)
                imprimir_con_delay(f'Se depositaron {cantidad} exitosamente')
                imprimir_con_delay(f'Nuevo saldo: {self.saldo}')
        except ValueError:
            imprimir_con_delay('Ingrese un número válido')
        
        return self.saldo
    
    def transferir_saldo(self):
        try:
            cantidad = int(input("Ingrese la cantidad a transferir: "))
            if cantidad > self.saldo:
                imprimir_con_delay('Saldo no disponible')
            else:
                imprimir_con_delay('Saldo transferido con éxito')
                self.saldo -= cantidad
                self.db.actualizar_saldo(self.id_usuario, self.saldo)
        except ValueError:
            imprimir_con_delay('Ingrese un número válido')
        
        return self.saldo


class Cajero:
    def __init__(self):
        self.db = BaseDeDatos()
        self.usuario_actual = None
    
    def opciones(self):
        try:
            opcion = int(input("""A continuación, seleccione la operación que desea realizar
                1 - Consultar saldo
                2 - Retirar saldo
                3 - Transferir
                4 - Depositar saldo
                5 - Crear nuevos usuarios
                6 - Mostrar usuarios registrados
                7 - Salir
            """))
            return opcion
        
        except ValueError:
            imprimir_con_delay('Seleccione una opción válida')
            return None
    
    def terminar_programa(self):
        imprimir_con_delay('Saliendo del sistema')
        self.db.cerrar_conexion()
    
    def mostrar_usuarios_registrados(self):
        """Muestra la lista de usuarios registrados en el sistema"""
        usuarios = self.db.obtener_usuarios()
        if not usuarios:
            imprimir_con_delay("No hay usuarios registrados en el sistema.")
            return
            
        imprimir_con_delay("\n--- USUARIOS REGISTRADOS ---")
        for i, nombre in enumerate(usuarios, 1):
            imprimir_con_delay(f"{i}. {nombre}")
        imprimir_con_delay("-------------------------\n")
    
    def iniciar_cajero(self):
        try:
            self.db.conectar()
            self.db.crear_tabla_usuarios()
            
            if self.db.verificar_usuarios_existentes() == 0:
                self.db.crear_usuario_inicial()

            intentos = 3

            while intentos > 0:
                usuario = input('Ingrese su nombre de usuario: ')
                contraseña = str(input('Ingrese su contraseña: '))

                resultado = self.db.autenticar_usuario(usuario, contraseña)

                if resultado:
                    id_usuario, saldo = resultado
                    imprimir_con_delay(f'Bienvenido {usuario}')
                    self.usuario_actual = Usuario(id_usuario, usuario, saldo, self.db)

                    while True:
                        opcion = self.opciones()
                        if opcion == 1:
                            self.usuario_actual.consultar_saldo()
                        elif opcion == 2:
                            self.usuario_actual.retirar_saldo()
                        elif opcion == 3:
                            self.usuario_actual.transferir_saldo()
                        elif opcion == 4:
                            self.usuario_actual.depositar_saldo()
                        elif opcion == 5:
                            imprimir_con_delay('Iniciando creación de usuarios...')
                            generar_usuarios()
                        elif opcion == 6:
                            self.mostrar_usuarios_registrados()
                        elif opcion == 7:
                            self.terminar_programa()
                            return
                        else:
                            imprimir_con_delay('Opción inválida. Intente de nuevo.')
                else:
                    intentos -= 1
                    imprimir_con_delay(f'Usuario o contraseña incorrectos. Intentos restantes: {intentos}')
                    if intentos == 0:
                        imprimir_con_delay('Demasiados intentos. Reinicie el programa e intente de nuevo.')
                        self.db.cerrar_conexion()
                        break
        finally:
            try:
                self.db.cerrar_conexion()
            except:
                pass

def generar_usuarios():
    db = BaseDeDatos()
    db.conectar()
    db.crear_tabla_usuarios()
    
    usuarios = []
    
    while True:
        try:
            crear_usuario = input('¿Desea crear un usuarios? (Si/No)')
            if crear_usuario.lower() == 'si':
                try:
                    nuevo_nombre_usuario = input('Ingrese el nombre del nuevo usuario: ')
                    
                    # Verificar si el usuario ya existe en la base de datos
                    if db.usuario_existe(nuevo_nombre_usuario):
                        imprimir_con_delay(f'El usuario "{nuevo_nombre_usuario}" ya existe. No se puede crear.')
                        continue
                        
                    nueva_contraseña_usuario = input('Ingrese la contraseña del nuevo usuario: ')
                    nuevo_saldo_usuario = float(input('Ingrese el saldo inicial del nuevo usuario: '))
                    
                    usuarios.append({
                        'nombre': nuevo_nombre_usuario,
                        'contraseña': nueva_contraseña_usuario,
                        'saldo': nuevo_saldo_usuario
                    })
                    
                    # Crear el usuario en la base de datos
                    db.crear_nuevo_usuario(nuevo_nombre_usuario, nueva_contraseña_usuario, nuevo_saldo_usuario)
                    
                    # No necesitamos crear un objeto Usuario aquí, solo estamos registrando usuarios
                    # El objeto Usuario se crea cuando alguien inicia sesión
                    imprimir_con_delay(f'Usuario {nuevo_nombre_usuario} creado con éxito')

                except ValueError:
                        print('Ingrese valores válidos')
                        continue
            else:
                break
        except ValueError:
            print('Ingrese una respuesta válida')
    
    db.cerrar_conexion()

def imprimir_con_delay(mensaje, delay=0.8):
    print(mensaje)
    time.sleep(delay)

if __name__ == "__main__":
    atm = Cajero()
    atm.iniciar_cajero()