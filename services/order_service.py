from pydantic import BaseModel
from confluent_kafka import Producer
import json
import logging

log = logging.getLogger("uvicorn")


app = create_fastapi_app()


class Order(BaseModel):
    cart: list


def delivery_report(err, msg):
    if err is not None:
        log.info("Message delivery failed: {err}")
    else:
        log.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")


@app.post("/order")
async def create_order(order: Order):
    p = Producer({'bootstrap.servers': 'localhost:9092'})
    data = order.dict()
    p.produce('orders', value=json.dumps(data), callback=delivery_report)
    p.flush()

    return {"message": "Order sent to Kafka"}
