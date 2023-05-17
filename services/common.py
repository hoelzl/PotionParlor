from configparser import ConfigParser
from typing import Callable
from confluent_kafka import Consumer, Producer, Message, TopicPartition
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import logging


def create_fastapi_app():
    app = FastAPI()

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def make_delivery_callback(client, log):
    def log_delivery_result(err, msg):
        if msg and msg.key():
            msg_key = msg.key().decode("utf-8")
        else:
            msg_key = None
        if err:
            log.info(f"{client}:delivery failed: key={msg_key}, error={err}")
        else:
            log.info(
                f"{client}:message delivered: "
                f"topic={msg.topic()}, key={msg_key}, part={msg.partition()}"
            )

    return log_delivery_result


def create_offset_commit_info(msg):
    return {
        "topic": msg.topic(),
        "partition": msg.partition(),
        "offset": msg.offset() + 1,
        "leader_epoch": msg.leader_epoch(),
    }


def make_committing_callback(client, log, consumer, commit_info):
    logging_callback = make_delivery_callback(client, log)

    def log_result_and_commit_offsets(err, msg):
        logging_callback(err, msg)
        if err:
            logging.error(f"{client}:delivery failure: {err}")
            raise Exception(f"Failed to deliver message to Kafka: {err}")
        else:
            logging.info(f":{client}:committing offsets: info={commit_info}")
            consumer.commit(offsets=[TopicPartition(**commit_info)])

    return log_result_and_commit_offsets


def read_config(config_file="config.ini", additional_sections=()):
    config_parser = ConfigParser()
    config_parser.read(config_file)
    config_dict = dict(config_parser["default"])
    for section in additional_sections:
        if config_parser.has_section(section):
            config_dict.update(config_parser[section])
    return config_dict


def create_consumer_and_producer(name, subscriptions):
    c = Consumer(read_config(additional_sections=[f"{name}.consumer"]))
    c.subscribe(subscriptions)

    p = Producer(read_config(additional_sections=[f"{name}.producer"]))
    return c, p


def run_processor(
    name: str,
    subscriptions: list[str],
    step_function: Callable[[Consumer, Producer, Message], None],
):
    logging.info(f"Starting {name} service")
    c, p = create_consumer_and_producer(name, subscriptions)
    # p.init_transactions()
    while True:
        try:
            # c.begin_transaction()
            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print(f"{name}:error: {msg.error()}")
                continue

            msg_topic, msg_key, msg_value = extract_msg_info(msg)
            logging.info(
                f"{name}:message received: "
                f"topic={msg_topic}, key={msg_key}, value={msg_value}"
            )
            try:
                step_function(c, p, msg)
            except json.decoder.JSONDecodeError as e:
                logging.error(f"{name}:invalid JSON: {e}")
            except Exception as e:
                logging.error(f"{name}:error while processing message: {e}")
            # c.commit_transaction()
        except KeyboardInterrupt:
            break
    c.close()


def extract_msg_info(msg):
    msg_topic = msg.topic()
    msg_key = msg.key().decode("utf-8") if msg.key() else None
    msg_value = msg.value().decode("utf-8")
    return msg_topic, msg_key, msg_value


known_potion_topics = [
    "invisibility",
    "flying",
    "healing",
    "strength",
    "intelligence",
]
