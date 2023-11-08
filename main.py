import requests
from bs4 import BeautifulSoup
import time
import logging
from datetime import datetime
import subprocess

# Configuración del registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
log_filename = 'cambios.log'
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))
logging.getLogger().addHandler(file_handler)

# URL de la página que deseas monitorear
url = ''

# Intervalo de tiempo entre verificaciones (en segundos, 5 segundos en este caso)
intervalo_de_verificacion = 5  # Verifica cada 5 segundos

# Variable para almacenar la versión anterior del contenido de la página web
contenido_anterior = ""

# Configura los encabezados de la solicitud para simular un navegador web
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': ''
}

# Función para verificar la página web en busca de cambios
def verificar_cambios():
    try:
        respuesta = requests.get(url, headers=headers)
        respuesta.raise_for_status()
        soup_actual = BeautifulSoup(respuesta.text, 'html.parser')
        contenido_actual = str(soup_actual)

        global contenido_anterior  # Accede a la variable global

        if contenido_actual != contenido_anterior:
            # Si se detecta un cambio, muestra la diferencia en el cmd y en el archivo de registro
            diferencia = contenido_anterior.splitlines(), contenido_actual.splitlines()
            for line in diferencia:
                print('Cambio en el contenido:', line)
                logging.info('Cambio en el contenido: %s', line)
            contenido_anterior = contenido_actual  # Actualiza el contenido anterior
            ejecutar_script_telegram()
            registrar_cambio()  # Registra el cambio en el registro

    except Exception as e:
        logging.error('Error al verificar la página web: %s', str(e))

# Función para ejecutar el script de Telegram
def ejecutar_script_telegram():
    try:
        subprocess.run(["python", "enviar_telegram.py", url])
    except Exception as e:
        logging.error('Error al ejecutar el script de Telegram: %s', str(e))

# Función para registrar cambios en el registro
def registrar_cambio():
    ahora = datetime.now()
    hora_actual = ahora.strftime('%Y-%m-%d %H:%M:%S')
    logging.info('Cambio detectado en la página web a las %s', hora_actual)

if __name__ == "__main__":
    while True:
        try:
            print('Iniciando verificación...')
            verificar_cambios()
            time.sleep(intervalo_de_verificacion)
        except KeyboardInterrupt:
            print('Verificación detenida por el usuario.')
            break
