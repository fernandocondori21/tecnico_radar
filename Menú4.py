import pymysql

def conectar(db_name):
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database=db_name
    )

def verificar_tecnico(nombre, apellido, matricula):
    conexion = conectar("serviciostecnicos")
    cursor = conexion.cursor()
    
    sql = "SELECT * FROM Tecnicos WHERE nombre = %s AND apellido = %s AND matricula = %s"
    cursor.execute(sql, (nombre, apellido, matricula))
    resultado = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    
    return resultado

def ingresar_tecnico():
    nombre = input("Ingrese nombre: ")
    apellido = input("Ingrese apellido: ")
    matricula = input("Ingrese matrícula: ")
    
    if verificar_tecnico(nombre, apellido, matricula):
        nro_documento = input("Ingrese número de documento: ")
        fecha_nacimiento = input("Ingrese fecha de nacimiento (YYYY-MM-DD): ")
        telefono = input("Ingrese teléfono: ")
        domicilio = input("Ingrese domicilio: ")
        
        try:
            conexion = conectar("SistemaGestion")
            cursor = conexion.cursor()
            
            sql = "INSERT INTO Tecnicos (nombre, apellido, nro_documento, fecha_nacimiento, telefono, domicilio, matricula) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            valores = (nombre, apellido, nro_documento, fecha_nacimiento, telefono, domicilio, matricula)
            
            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()
            
            print("Datos del técnico ingresados correctamente.")
        except pymysql.MySQLError as e:
            print(f"Error al ingresar los datos: {e}")
    else:
        print("Error: Los datos del técnico no coinciden con los registrados.")

def ingresar_cliente():
    try:
        conexion = conectar("SistemaGestion")
        cursor = conexion.cursor()
        
        nombre = input("Ingrese nombre: ")
        apellido = input("Ingrese apellido: ")
        nro_documento = input("Ingrese número de documento: ")
        fecha_nacimiento = input("Ingrese fecha de nacimiento (YYYY-MM-DD): ")
        telefono = input("Ingrese teléfono: ")
        domicilio = input("Ingrese domicilio: ")
        
        sql = "INSERT INTO Clientes (nombre, apellido, nro_documento, fecha_nacimiento, telefono, domicilio) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (nombre, apellido, nro_documento, fecha_nacimiento, telefono, domicilio)
        
        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        print("Datos del cliente ingresados correctamente.")
    except pymysql.MySQLError as e:
        print(f"Error al ingresar los datos: {e}")

def consultar_datos():
    try:
        conexion = conectar("SistemaGestion")
        cursor = conexion.cursor()
        
        tabla = input("Consultar datos de (tecnicos/clientes): ").strip().lower()
        if tabla not in ["tecnicos", "clientes"]:
            print("Tabla no válida.")
            return
        
        sql = f"SELECT * FROM {tabla.capitalize()}"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        
        for fila in resultados:
            print(fila)
        
        cursor.close()
        conexion.close()
    except pymysql.MySQLError as e:
        print(f"Error al consultar los datos: {e}")

def eliminar_datos():
    try:
        conexion = conectar("SistemaGestion")
        cursor = conexion.cursor()
        
        tabla = input("Eliminar datos de (tecnicos/clientes): ").strip().lower()
        if tabla not in ["tecnicos", "clientes"]:
            print("Tabla no válida.")
            return

        try:
            id = int(input("Ingrese ID del registro a eliminar: "))
        except ValueError:
            print("El ID debe ser un número entero.")
            return
        
        sql = f"DELETE FROM {tabla.capitalize()} WHERE id = %s"
        
        cursor.execute(sql, (id,))
        conexion.commit()
        
        print("Datos eliminados correctamente.")
        cursor.close()
        conexion.close()
    except pymysql.MySQLError as e:
        print(f"Error al eliminar los datos: {e}")

def ordenar_datos():
    try:
        conexion = conectar("SistemaGestion")
        cursor = conexion.cursor()
        
        tabla = input("Ordenar datos de (tecnicos/clientes): ").strip().lower()
        if tabla not in ["tecnicos", "clientes"]:
            print("Tabla no válida.")
            return

        criterio = input("Ordenar por (nombre/apellido/id/edad): ").strip().lower()
        if criterio not in ["nombre", "apellido", "id", "edad"]:
            print("Criterio no válido.")
            return

        if criterio == "edad":
            criterio = "fecha_nacimiento"
        
        sql = f"SELECT * FROM {tabla.capitalize()} ORDER BY {criterio}"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        
        for fila in resultados:
            print(fila)
        
        cursor.close()
        conexion.close()
    except pymysql.MySQLError as e:
        print(f"Error al ordenar los datos: {e}")

def menu():
    while True:
        print("\n--- Menú de Gestión ---")
        print("1. Ingreso de datos (Técnicos)")
        print("2. Ingreso de datos (Clientes)")
        print("3. Consulta de datos")
        print("4. Eliminación de datos")
        print("5. Ordenamiento de datos")
        print("6. Salida")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            ingresar_tecnico()
        elif opcion == "2":
            ingresar_cliente()
        elif opcion == "3":
            consultar_datos()
        elif opcion == "4":
            eliminar_datos()
        elif opcion == "5":
            ordenar_datos()
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
