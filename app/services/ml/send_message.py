import pika
import uuid
from decouple import config


# Параметры подключения
connection_params = pika.ConnectionParameters(
    host=config('RABBITMQ_HOST'),
    port=int(config('RABBITMQ_PORT')),
    virtual_host='/',
    credentials=pika.PlainCredentials(
        username=config('RABBITMQ_USERNAME'),
        password=config('RABBITMQ_PASSWORD')
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)


def send_message(message):
    response = None
    # Установка соединения
    connection = pika.BlockingConnection(connection_params)
    # Создание канала
    channel = connection.channel()
    # Имя очереди
    queue_name = 'days_in_sheter_predict'
    # Отправка сообщения
    channel.queue_declare(queue=queue_name)  # Создание очереди (если не существует)
    # Создание временной очереди для ответов
    result_queue = channel.queue_declare(queue='', exclusive=True).method.queue
    # Генерация уникального идентификатора для запроса
    correlation_id = str(uuid.uuid4())
    # Отправка сообщения
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        properties=pika.BasicProperties(reply_to=result_queue,
                                        correlation_id=correlation_id),
        body=message)

    # Функция для обработки ответа
    def on_response(ch, method, properties, body):
        if properties.correlation_id == correlation_id:
            # Дополнительная обработка ответа
            channel.basic_cancel(consumer_tag=consumer_tag)
            # Удаление очереди
            channel.queue_delete(queue=result_queue)
            # Закрытие соединения
            connection.close()
            nonlocal response
            response = body.decode('utf-8')  # Декодирование байтовой строки в обычную строку

    # Запуск ожидания ответов
    consumer_tag = channel.basic_consume(queue=result_queue, on_message_callback=on_response, auto_ack=True)
    channel.start_consuming()
    return response


# import json
# try:
#     animal_input = {"name": 1,
#                     "intake_type": 'Wildlife',
#                     "intake_condition": 'Injured',
#                     "animal_type": 'Bird',
#                     "sex_upon_intake": 'Unknown',
#                     "age_upon_intake": 730,
#                     "mixed_color": 1,
#                     "first_color": 'Yellow',
#                     "second_color": 'Yellow',
#                     "mixed_breed": 0,
#                     "first_breed": 'Hawk',
#                     "second_breed": 'Not'}
#     animal_json = json.dumps(animal_input)
#     result = send_message(animal_json)
#     print(result)
# except Exception as e2:
#     print(e2)