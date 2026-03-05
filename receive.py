#!/usr/bin/env python
import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='unachlidts')

    def callback(ch, method, properties, body):
        mensaje = body.decode('utf-8')  
        print(f" [x] Received {mensaje}")
    
        with open("mensajes_recibidos.txt", "a", encoding="utf-8") as f:
            f.write(mensaje + "\n")

    channel.basic_consume(queue='unachlidts', on_message_callback=callback, auto_ack=True)

    print(' [*] Esperando mensajes. Presione  CTRL+C para salir')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)