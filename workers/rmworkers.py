import pika
import threading
import json
from joblib import load
import pandas as pd
from pydantic import ValidationError
from models.schema import AnimalInput
from decouple import config


# Загрузка модели
model = load("./model_regressor")


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



# Валидация входных данных
def handler1(ch, method, properties, body):
    try:
        data_str = body.decode('utf-8')
        data_dict = json.loads(data_str)
        animal_input = AnimalInput(**data_dict)
        # Если данные прошли валидацию, продолжаем обработку
        handler2(ch, method, properties, animal_input)
    except ValidationError as e:
        # Если данные не прошли валидацию, обработка прерывается
        response = f"Invalid data: {e}"
        correlation_id = properties.correlation_id
        ch.basic_publish(
            exchange='',
            routing_key=reply_to,
            properties=pika.BasicProperties(correlation_id=correlation_id),
            body=response
        )


# Предсказание
def handler2(ch, method, properties, animal_input):
    animal_input_dict = animal_input.dict()
    animal_input_df = pd.DataFrame(animal_input_dict, index=[0])
    days_in_shelter = model.predict(animal_input_df)[0]
    handler3(ch, method, properties, days_in_shelter)


# Запись результата
def handler3(ch, method, properties, days_in_shelter):
    correlation_id = properties.correlation_id
    reply_to = properties.reply_to
    days_in_shelter_str = str(days_in_shelter)

    ch.basic_publish(
        exchange='',
        routing_key=reply_to,
        properties=pika.BasicProperties(correlation_id=correlation_id),
        body=days_in_shelter_str
    )

    print("Ответ отправлен во временную очередь")


def callback(ch, method, properties, body):
    handler1(ch, method, properties, body)


def worker():
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.queue_declare(queue='days_in_sheter_predict')
    channel.basic_consume(queue='days_in_sheter_predict', on_message_callback=callback, auto_ack=True)
    print("Worker started")
    channel.start_consuming()


nworkers = int(config('NWORKERS'))

# Создаем несколько воркеров
for i in range(nworkers):
    threading.Thread(target=worker).start()
