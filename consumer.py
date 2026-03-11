import pika
import sys

def callback(ch, method, properties, body):
    mensaje = body.decode('utf-8')
    print(f" [x] RabbitMQ recibió: {mensaje}")
    
    with open("mensajes_recibidos.txt", "a", encoding="utf-8") as file:
        file.write(mensaje + "\n")
        
    print(" [✓] Log guardado exitosamente en mensajes_recibidos.txt")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='seguridad_logs', durable=True)
    print(' [*] Consumidor de logs activo. Esperando mensajes...')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='seguridad_logs', on_message_callback=callback)

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Saliendo...')
        sys.exit(0)