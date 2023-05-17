import json
import logging

from common import make_delivery_callback, known_potion_topics, run_processor

logging.basicConfig(level=logging.INFO)


def process_message(producer, msg_topic, msg_key, msg_value):
    if msg_topic == "orders":
        dispatch_order(producer, msg_key, msg_value)
    else:
        logging.info(f"Unknown topic: {msg_topic}")


def dispatch_order(producer, msg_key, msg_value):
    order = json.loads(msg_value)
    for item in order["line_items"]:
        topic = item["potion"].lower()
        if topic not in known_potion_topics:
            topic = "unknown-potions"
        producer.produce(
            topic,
            key=msg_key,
            value=json.dumps(item),
            on_delivery=make_delivery_callback("dispatcher", logging),
        )


if __name__ == "__main__":
    run_processor("dispatcher", ["orders"], process_message)
