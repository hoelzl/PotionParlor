# Potion Parlor

A simple example to show how to use Kafka to distribute messages between
microservices.

## Running Manually

Currently there is no docker-compose file to run the entire application. You
will need to run each service manually:

| Directory           | Command                                          |
|:--------------------| :---------------------                           |
| `kafka-cluster`     | `docker-compose up -d`                           |
| `tools`             | `python create_topics.py`(*)                     |
| `web/potion-parlor` | `node install`(*)                                |
|                     | `npm start`                                      |
| `services`          | `uvicorn order_service:app --port 3001 --reload` |
| `services`          | `python dispatcher.py`                           |
| `services`          | `python brewer.py`                               |

The commands marked with (*) only need to be run once.

Then browse to <http://localhost:3000> and order potions!
