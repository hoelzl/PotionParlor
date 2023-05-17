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
        data = json.loads(msg_value)
        num_images = data.get("quantity", 1)
        image = {
            "quantity": num_images,
            "order_id": data.get("order_id", 0),
            "image_path": "/home/tc/tmp/img-default.png"
        }
        commit_info = create_offset_commit_info(msg)
        note_image_printed(
            consumer, producer, order_id=msg_key, potion=image, commit_info=commit_info
        )
    else:
        logging.info(f"image-generator:unknown topic: {msg_topic}")


def note_image_printed(consumer, producer, order_id, potion, commit_info):
    topic = "printed-images"
    producer.produce(
        topic,
        key=order_id,
        value=json.dumps({"order_id": order_id, **potion}),
        on_delivery=make_committing_callback("image-generator", logging, consumer, commit_info),
    )
    producer.flush()


if __name__ == "__main__":
    run_processor("image-generator", known_potion_topics, process_message)
