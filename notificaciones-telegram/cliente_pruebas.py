import pika
import shutil
import configparser
import argparse

def procesar(bot,canal_id,texto,foto,nombre_canal_rabbit):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=nombre_canal_rabbit)

    mensaje=bot+"#"+canal_id+"#"+texto+"#"+foto

    channel.basic_publish(exchange="", routing_key=nombre_canal_rabbit, body=mensaje)

    channel.confirm_delivery()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Inicia el pipeline de pruebas')
    parser.add_argument('archivo_configuracion')

    args = vars(parser.parse_args())
    archivo_configuracion = args['archivo_configuracion']

    config = configparser.ConfigParser()
    config.read(archivo_configuracion)
    
    bot = config['TELEGRAM']['bot']
    canal_id = config['TELEGRAM']['canal_id']
    foto = config['MENSAJE']['foto']
    texto = config['MENSAJE']['texto']

    nombre_canal_rabbit = config['RABBIT']['nombre_canal']

    procesar(bot,canal_id,texto,foto,nombre_canal_rabbit)