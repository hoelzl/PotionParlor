from confluent_kafka.admin import AdminClient, NewTopic

a = AdminClient({"bootstrap.servers": "localhost:9092"})

new_topics = [NewTopic("orders", num_partitions=3, replication_factor=1)]
fs = a.create_topics(new_topics)

for topic, f in fs.items():
    try:
        f.result()
        print("Topic {} created".format(topic))
    except Exception as e:
        print("Failed to create topic {}: {}".format(topic, e))
