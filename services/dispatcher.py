import json
import logging

from common import (
    extract_msg_info,
    known_potion_topics,
    make_delivery_callback,
    run_processor,
)

logging.basicConfig(level=logging.INFO)


def process_message(consumer, producer, msg):
    msg_topic, msg_key, msg_value = extract_msg_info(msg)
    if msg_topic == "orders":
        dispatch_order(producer, msg_key, msg_value)
    else:
        logging.info(f"dispatcher:unknown topic: {msg_topic}")


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
