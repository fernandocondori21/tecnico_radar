import requests
from bs4 import BeautifulSoup
import pymysql

# Función para obtener datos básicos de la tabla
def obtener_datos_tabla(soup):
    matriculados = []
    filas = soup.select('tbody.VUpDdz._2DI6N.wixui-table__body tr')
    for fila in filas:
        datos = fila.find_all('td')
        if len(datos) == 6:
            foto_elem = datos[0].find('img')
            foto = foto_elem['src'] if foto_elem and 'src' in foto_elem.attrs else "N/A"
            apellido = datos[1].text.strip()
            nombre = datos[2].text.strip()
            provincia = datos[3].text.strip()
            departamento = datos[4].text.strip()
            matricula = datos[5].text.strip()
            matriculados.append({
                'foto': foto,
                'apellido': apellido,
                'nombre': nombre,
                'provincia': provincia,
                'departamento': departamento,
                'matricula': matricula
            })
    return matriculados

# Función para obtener detalles adicionales de un técnico
def obtener_detalles_tecnico(url_base, tecnico):
    response = requests.get(url_base)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        detalles = soup.find_all('div', class_='comp-k3whqsno')
        for detalle in detalles:
            apellido_elem = detalle.find('h4', style='font-size:24px; text-align:right;')
            if apellido_elem and apellido_elem.text.strip() == tecnico['apellido']:
                telefono_elem = detalle.find('p', class_='font_7')
                email_elem = detalle.find('a', href=True)
                tipo_formacion_elem = detalle.find_all('p', class_='font_7')[1] if len(detalle.find_all('p', class_='font_7')) > 1 else None
                tecnico['telefono'] = telefono_elem.text.strip() if telefono_elem else "N/A"
                tecnico['email'] = email_elem['href'].replace('mailto:', '').strip() if email_elem else "N/A"
                tecnico['tipo_formacion'] = tipo_formacion_elem.text.strip() if tipo_formacion_elem else "N/A"
    return tecnico

# URL base de la página web
url_base = 'https://www.camaraargentinaderefrigeracion.com/matriculados'

# Hacer una solicitud a la página web
response = requests.get(url_base)
print(f"Estado de la respuesta: {response.status_code}")

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    matriculados = obtener_datos_tabla(soup)
    print(f"Número de matriculados encontrados: {len(matriculados)}")
    
    # Conectar a la base de datos
    try:
        conexion = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="serviciostecnicos"
        )
        print("Conexión exitosa a la base de datos MySQL")
    except pymysql.MySQLError as err:
        print(f"Error al conectar a la base de datos: {err}")
        exit()

    cursor = conexion.cursor()
    
    # Obtener y insertar datos de cada técnico
    for tecnico in matriculados:
        tecnico_completo = obtener_detalles_tecnico(url_base, tecnico)
        try:
            sql = "INSERT INTO Tecnicos (apellido, nombre, provincia, departamento, telefono, email, tipo_formacion, matricula, nro_documento, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            valores = (
                tecnico_completo['apellido'],
                tecnico_completo['nombre'],
                tecnico_completo['provincia'],
                tecnico_completo['departamento'],
                tecnico_completo.get('telefono', 'N/A'),
                tecnico_completo.get('email', 'N/A'),
                tecnico_completo.get('tipo_formacion', 'N/A'),
                tecnico_completo['matricula'],
                'N/A',
                tecnico_completo['foto']
            )
            cursor.execute(sql, valores)
        except Exception as e:
            print(f"Error al insertar técnico: {e}")

    conexion.commit()
    print("Datos insertados correctamente.")
    
    # Cerrar la conexión
    cursor.close()
    conexion.close()
    print("Conexión a la base de datos cerrada")
else:
    print("Error al acceder a la página.")
