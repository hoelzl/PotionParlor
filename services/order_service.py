from pydantic import BaseModel
from confluent_kafka import Producer
import json
import logging

from common import create_fastapi_app, make_delivery_callback, read_config

log = logging.getLogger("uvicorn")
app = create_fastapi_app()


class Order(BaseModel):
    line_items: list
    order_id: int | None = None


@app.post("/order")
async def create_order(order: Order):
    p = Producer(read_config(additional_sections=["order-service"]))
    data = order.dict()
    if data:
        order_id = f"{data.get('order_id', 1):08}"
    else:
        order_id = "0" * 8
    data["order_id"] = order_id
    log.info(f"Sending order to Kafka: {order_id}, {data['line_items']}")
    p.produce(
        "received-orders",
        key=order_id,
        value=json.dumps(
            {"order_id": order_id, "num_line_items": len(data["line_items"])}
        ),
        on_delivery=make_delivery_callback("order-service", log),
    )
    p.produce(
        "orders",
        key=order_id,
        value=json.dumps(data),
        on_delivery=make_delivery_callback("order-service", log),
    )
    p.flush()

    return {"message": "Order sent to Kafka"}
