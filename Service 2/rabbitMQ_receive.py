import pika, sys, os
import mongodb_module
import imagga_module
import mailgun_module

AMQP_URL = "your_ampq_url"


def process_ad_image(ad_id):
    ad_mongo_doc = mongodb_module.get_ad_by_id(ad_id)
    ad_s3_url = ad_mongo_doc['url']
    image_category = imagga_module.process_image(ad_s3_url, 'vehicle')

    if image_category is not None:
        mongodb_module.update_doc_field(ad_id, 'category', image_category)
        mongodb_module.update_doc_field(ad_id, 'state', 'approved')
        updated_ad = mongodb_module.get_ad_by_id(ad_id)
        # print('Ad approved')

        return updated_ad

    else:
        mongodb_module.update_doc_field(ad_id, 'state', 'rejected')
        updated_ad = mongodb_module.get_ad_by_id(ad_id)
        # print('Ad rejected')

        return updated_ad


def send_ad_status_email(ad_doc):
    ad_id = ad_doc['id']
    ad_email = ad_doc['email']
    ad_state = ad_doc['state']
    email_text = f'Your advertisement with id: {ad_id} was {ad_state}'
    mailgun_module.send_email(ad_email, email_text)


def rabbitmq_receive():
    connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        ad_id = int(body.decode())

        final_doc = process_ad_image(ad_id)
        send_ad_status_email(final_doc)
        print('processed ad with id : ', ad_id)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        rabbitmq_receive()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
