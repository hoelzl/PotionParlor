from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from confluent_kafka import Producer
import json
import logging

log = logging.getLogger("uvicorn")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
