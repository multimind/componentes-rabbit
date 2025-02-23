import pika
import configparser
import os
import logging
import argparse
import time
import requests

def callback(ch, method, properties, body):
    print(f"Received: {body.decode()}")

    mensaje=body.decode()

    print(mensaje)
    partes=mensaje.split("#")

    bot=partes[0]
    canal_id=partes[1]
    mensaje=partes[2]
    ruta_imagen=partes[3]

    print("bot")
    print(bot)

    print("canal_id")
    print(canal_id)

    print("mensaje")
    print(mensaje)

    print("ruta_imagen")
    print(ruta_imagen)

    url_telegram="https://api.telegram.org/bot"+bot

    url = url_telegram + "/sendPhoto?chat_id=" + canal_id + "&text=" + mensaje

    archivo=open(ruta_imagen,"rb")

    files={'photo': archivo}
    values={'mimetype':'image/jpg','caption':mensaje }

    response = requests.post(url,files=files,data=values)

    archivo.close()
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def procesar(config):    
    nombre_canal=config["RABBIT_ENTRADA"]["nombre_canal"]

    while True:
        try:
    
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()

            channel.queue_declare(queue=nombre_canal)

            channel.basic_consume(queue=nombre_canal, on_message_callback=callback)

            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError as e:
            print(f"Connection error: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)
        except pika.exceptions.ChannelClosedByBroker as e:
            print(f"Channel closed by broker: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(e)
            print(f"Unexpected error: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Inicia el servidor de procesamiento notificaciones telegram')
    parser.add_argument('archivo_configuracion')

    args = vars(parser.parse_args())
    archivo_configuracion = args['archivo_configuracion']

    config = configparser.ConfigParser()
    config.read(archivo_configuracion)

    procesar(config)
