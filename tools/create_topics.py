from confluent_kafka.admin import AdminClient, NewTopic

a = AdminClient({"bootstrap.servers": "localhost:9092"})

new_topics = [
    NewTopic("orders", num_partitions=3, replication_factor=1),
    NewTopic("invisibility", num_partitions=3, replication_factor=1),
    NewTopic("flying", num_partitions=3, replication_factor=1),
    NewTopic("healing", num_partitions=3, replication_factor=1),
    NewTopic("strength", num_partitions=3, replication_factor=1),
    NewTopic("intelligence", num_partitions=3, replication_factor=1),
]
fs = a.create_topics(new_topics)

for topic, f in fs.items():
    try:
        f.result()
        print(f"Topic {topic} created")
    except Exception as e:
        print(f"Failed to create topic {topic}: {e}")
