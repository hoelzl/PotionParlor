import json
import logging

from common import (
    create_offset_commit_info,
    extract_msg_info,
    known_potion_topics,
    make_committing_callback,
    run_processor,
)

logging.basicConfig(level=logging.INFO)


def process_message(consumer, producer, msg):
    msg_topic, msg_key, msg_value = extract_msg_info(msg)

    if msg_topic in known_potion_topics:
        potion_type = msg_topic
        data = json.loads(msg_value)
        num_bottles = data.get("quantity", 1)
        potion = {
            "potion_type": potion_type,
            "quantity": num_bottles,
            "order_id": data.get("order_id", 0),
        }
        commit_info = create_offset_commit_info(msg)
        note_potion_brewed(
            consumer, producer, order_id=msg_key, potion=potion, commit_info=commit_info
        )
    else:
        logging.info(f"brewer:unknown topic: {msg_topic}")


def note_potion_brewed(consumer, producer, order_id, potion, commit_info):
    topic = "brewed-potions"
    producer.produce(
        topic,
        key=order_id,
        value=json.dumps({"order_id": order_id, **potion}),
        on_delivery=make_committing_callback("brewer", logging, consumer, commit_info),
    )
    producer.flush()


if __name__ == "__main__":
    run_processor("brewer", known_potion_topics, process_message)
