#Note:  Confluent_kafka only supported for Python 3.7 or older
import time
from kafka import KafkaProducer
from kafka import KafkaConsumer, TopicPartition

# Producer

msg = ('kafkakafkakafka' * 20).encode()[:100]
size = 1000000
producer = KafkaProducer(bootstrap_servers='localhost:9092')

def kafka_python_producer_sync(producer, size):
    for _ in range(size):
        future = producer.send('topic', msg)
        result = future.get(timeout=60)
    producer.flush()
    
def success(metadata):
    print(metadata.topic)

def error(exception):
    print(exception)

def kafka_python_producer_async(producer, size):
    for _ in range(size):
        producer.send('topic', msg).add_callback(success).add_errback(error)
    producer.flush()

# Consumer

size = 1000000

consumer1 = KafkaConsumer(bootstrap_servers='localhost:9092')
def kafka_python_consumer1():
    consumer1.subscribe(['topic1'])
    for msg in consumer1:
      print(msg)

consumer2 = KafkaConsumer(bootstrap_servers='localhost:9092')
def kafka_python_consumer2():
    consumer2.assign([TopicPartition('topic1', 1), TopicPartition('topic2', 1)])
    for msg in consumer2:
        print(msg)

consumer3 = KafkaConsumer(bootstrap_servers='localhost:9092')
def kafka_python_consumer3():
    partition = TopicPartition('topic3', 0)
    consumer3.assign([partition])
    last_offset = consumer3.end_offsets([partition])[partition]
    for msg in consumer3:
        if msg.offset == last_offset - 1:
            break



#%%
# Producer
from confluent_kafka import Producer
from python_kafka import Timer
from confluent_kafka import Consumer, TopicPartition

producer = Producer({'bootstrap.servers': 'localhost:9092'})
msg = ('kafkatest' * 20).encode()[:100]
size = 1000000

def delivery_report(err, decoded_message, original_message):
    if err is not None:
        print(err)

def confluent_producer_async():
    for _ in range(size):
        producer.produce(
            "topic1",
            msg,
            callback=lambda err, decoded_message, original_message=msg: delivery_report(  # noqa
                err, decoded_message, original_message
            ),
        )
    producer.flush()
    
def confluent_producer_sync():
    for _ in range(100000):
        producer.produce(
            "topic1",
            msg,
            callback=lambda err, decoded_message, original_message=msg: delivery_report(  # noqa
                err, decoded_message, original_message
            ),
        )
        producer.flush()

# Consumer

size = 1000000

consumer = Consumer(
    {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest',
    }
)

def consume_session_window(consumer, timeout=1, session_max=5):
    session = 0
    while True:
        message = consumer.poll(timeout)
        if message is None:
            session += 1
            if session > session_max:
                break
            continue
        if message.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        yield message
    consumer.close() 
            
def consume(consumer, timeout):
    while True:
        message = consumer.poll(timeout)
        if message is None:
            continue
        if message.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        yield message
    consumer.close()

def confluent_consumer():
    consumer.subscribe(['topic1'])
    for msg in consume(consumer, 1.0):
        print(msg)

def confluent_consumer_partition():
    consumer.assign([TopicPartition("topic1", 0)])
    for msg in consume(consumer, 1.0):
        print(msg)


#%%
# Producer
from pykafka import KafkaClient
from pykafka.simpleconsumer import OffsetType

client = KafkaClient(hosts="localhost:9092")
topic = client.topics[b'topic1']
msg = ('kafkatest' * 20).encode()[:100]

def pykafka_producer_sync(size):
    with topic.get_sync_producer() as producer:
        for i in range(size):
            producer.produce(msg)
        producer.stop()

def pykafka_producer_async(size):
    with topic.get_producer() as producer:
        for i in range(size):
            producer.produce(msg)
        producer.stop()

def pykafka_producer_async_report(size):
    with topic.get_producer(delivery_reports=True, min_queued_messages=1) as producer:
        for i in range(size):
            producer.produce(msg)
            while True:
                try:
                    report, exc = producer.get_delivery_report(block=False)
                    print(report)
                except Exception:
                    break
        producer.stop()
        
# Consumer
client = KafkaClient(hosts="localhost:9092")
topic = client.topics[b'topic1']

def pykafka_consumer():
    consumer = topic.get_simple_consumer(consumer_group="mygroup", auto_offset_reset=OffsetType.EARLIEST)
    for message in consumer:
        print(message)



