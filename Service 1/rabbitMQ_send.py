import pika

AMQP_URL = "your_amqp_url"


def rabbitmq_send(ad_id):
    connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body=ad_id)
    print(" [x] Sent {}".format(ad_id))
    connection.close()
