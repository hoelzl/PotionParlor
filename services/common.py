from configparser import ConfigParser
from typing import Callable
from confluent_kafka import Consumer, Producer
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


def make_delivery_callback(producer, log):
    def log_delivery_result(err, msg):
        if msg and msg.key():
            msg_key = msg.key().decode("utf-8")
        else:
            msg_key = None
        if err:
            log.info(f"{producer}:delivery failed: key={msg_key}, error={err}")
        else:
            log.info(
                f"{producer}:message delivered: "
                f"topic={msg.topic()}, key={msg_key}, part={msg.partition()}"
            )

    return log_delivery_result


def read_config(config_file="config.ini", additional_sections=()):
    config_parser = ConfigParser()
    config_parser.read(config_file)
    config_dict = dict(config_parser["default"])
    for section in additional_sections:
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
    step_function: Callable[[Producer, str, str | None, str], None],
):
    logging.info(f"Starting {name} service")
    c, p = create_consumer_and_producer(name, subscriptions)
    while True:
        try:
            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print(f"{name}:error: {msg.error()}")
                continue

            msg_topic = msg.topic()
            msg_key = msg.key().decode("utf-8") if msg.key() else None
            msg_value = msg.value().decode("utf-8")
            logging.info(
                f"{name}:message received: "
                f"topic={msg_topic}, key={msg_key}, value={msg_value}"
            )
            try:
                step_function(p, msg_topic, msg_key, msg_value)
            except json.decoder.JSONDecodeError as e:
                logging.error(f"{name}:invalid JSON: {e}")
            except Exception as e:
                logging.error(f"{name}:error while processing message: {e}")
            p.flush()
        except KeyboardInterrupt:
            break
    c.close()


known_potion_topics = [
    "invisibility",
    "flying",
    "healing",
    "strength",
    "intelligence",
]
