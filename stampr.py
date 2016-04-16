#!/usr/bin/env python
import pika

count = 0

def callback(unused_channel, basic_deliver, properties, message):
        # forward to connector and post back a success message
        print(" [x] Received %r" % message)
        print('unused_channel='+repr(unused_channel))
        print('basic_deliver' + repr(basic_deliver))
        print('properties='+repr(properties))
        print('unused_channel='+repr(unused_channel))
        credentials = pika.PlainCredentials("guest","guest")
        parameters = pika.ConnectionParameters("localhost",
                                       5672,
                                       "/",
                                       credentials)
        print('2')
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        if "JIRA-101" not in message:
            channel.basic_publish('rajamani_mq_exchange',
                      'cifs_connector_queue',
                      "JIRA-101" + message,
                      pika.BasicProperties(content_type='text/plain',
                                           delivery_mode=1))
        else:
            #count = count + 1
            print('count of messages' + str('One'))
        print(' [x] Sent ' + message)


def receive():
    credentials = pika.PlainCredentials("guest","guest")
    parameters = pika.ConnectionParameters("localhost",
                                       5672,
                                       "/",
                                       credentials)
    print('1')
    connection = pika.BlockingConnection(parameters)

    print('2')
    channel = connection.channel()

    print('3')
    channel.queue_declare(queue='cifs_connector_queue')

    print('4')
    channel.basic_consume(callback, 'cifs_connector_queue')


    print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    try:
       channel.start_consuming()
    except KeyboardInterrupt:
       channel.stop_consuming()
    connection.close()


receive()
