# Potion Parlor

A simple example to show how to use Kafka to distribute messages between
microservices.

## Running Manually

Currently there is no docker-compose file to run the entire application. You
will need to run each service manually:

| Directory           | Command                                          |
| :------------------ | :---------------------                           |
| `kafka-cluster`     | `docker-compose up -d`                           |
| `web/potion-parlor` | `npm start`                                      |
| `order-service`     | `uvicorn order_service:app --port 3001 --reload` |
| `dispatcher`        | `python dispatcher.py`                           |

Then browse to [http://localhost:3000] and order potions!