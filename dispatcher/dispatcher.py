from confluent_kafka import Consumer, Producer
import json
import logging

logging.basicConfig(level=logging.INFO)

# Consumer setup
c = Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": "dispatcher",
        "auto.offset.reset": "earliest",
    }
)

c.subscribe(["orders"])

# Producer setup
p = Producer({"bootstrap.servers": "localhost:9092"})


def delivery_report(err, msg):
    if err is not None:
        logging.info("Message delivery failed: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")


while True:
    try:
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        msg_value = msg.value().decode("utf-8")
        logging.info(f"Message received: {msg_value}")
        try:
            order = json.loads(msg_value)
            for item in order["cart"]:
                p.produce(
                    item["potion"].lower(), json.dumps(item), callback=delivery_report
                )
        except json.decoder.JSONDecodeError as e:
            logging.error(f"Invalid JSON: {e}")

        p.flush()
    except KeyboardInterrupt:
        break

c.close()
