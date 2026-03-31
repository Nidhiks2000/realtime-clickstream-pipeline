import time
import random
import uuid
import json
from datetime import datetime, timezone
import os

from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField

base_dir = os.path.dirname(os.path.abspath(__file__))
ca_path = os.path.join(base_dir, 'ca.pem')


KAFKA_SERVICE_URI = '<kafka_host>:14710'
SCHEMA_REGISTRY_URI = 'https://<kafka_host>:14702'
USERNAME = 'avnadmin'
PASSWORD = <password>
CA_PEM_PATH = ca_path  

TOPIC_NAME = 'clickstream'
SCHEMA_SUBJECT = 'clickstream-data' 


common_conf = {
    'bootstrap.servers': KAFKA_SERVICE_URI,
    'security.protocol': 'SASL_SSL',      
    'sasl.mechanisms': 'SCRAM-SHA-256',
    'sasl.username': USERNAME,
    'sasl.password': PASSWORD,
    'ssl.ca.location': ca_path,          
}


def create_topic_if_not_exists():
    """Checks for the topic and creates it if missing."""
    admin_client = AdminClient(common_conf)
    topic_metadata = admin_client.list_topics(timeout=10)
    
    if TOPIC_NAME not in topic_metadata.topics:
        print(f"Topic '{TOPIC_NAME}' not found. Creating...")
        new_topic = NewTopic(TOPIC_NAME, num_partitions=3, replication_factor=3)
        fs = admin_client.create_topics([new_topic])
        # Wait for operation to finish
        for topic, f in fs.items():
            try:
                f.result()
                print(f"Topic {topic} created successfully.")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")
    else:
        print(f"Topic '{TOPIC_NAME}' already exists.")

def generate_click_event():
    """Generates a meaningful clickstream event with ISO 8601 timestamp."""
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
        "event_id": str(uuid.uuid4()),
        "user_id": f"user_{random.randint(100, 999)}",
        "session_id": str(uuid.uuid4()),
        "action": random.choice(['view_page', 'add_to_cart', 'search', 'purchase']),
        "page_url": random.choice(['/home', '/products/123', '/cart', '/checkout']),
        "device": random.choice(['mobile', 'desktop', 'tablet']),
        "browser": random.choice(['Chrome', 'Safari', 'Firefox']),
        "response_time_ms": random.randint(40, 450),
        "geo_location": random.choice(['US', 'UK', 'DE', 'IN', 'CA'])
    }


def main():
    create_topic_if_not_exists()

    sr_conf = {
        'url': SCHEMA_REGISTRY_URI,
        'basic.auth.user.info': f"{USERNAME}:{PASSWORD}"
    }
    sr_client = SchemaRegistryClient(sr_conf)

    # Fetch the schema you manually created
    print(f"Fetching latest schema for subject: {SCHEMA_SUBJECT}...")
    schema_metadata = sr_client.get_latest_version(SCHEMA_SUBJECT)
    schema_str = schema_metadata.schema.schema_str

    # Set up Serializers
    avro_serializer = AvroSerializer(sr_client, schema_str)
    string_serializer = StringSerializer('utf_8')

    # Initialize Producer
    producer = Producer(common_conf)

    print(f"Starting stream to Aiven Kafka. Press Ctrl+C to stop.")

    try:
        while True:
            event = generate_click_event()
            
            # Produce the Avro message
            producer.produce(
                topic=TOPIC_NAME,
                key=string_serializer(event['user_id']),
                value=avro_serializer(event, SerializationContext(TOPIC_NAME, MessageField.VALUE)),
                on_delivery=lambda err, msg: print(f"Event sent: {msg.key().decode('utf-8')}") if err is None else print(f"Error: {err}")
            )
            
            producer.poll(0)
            time.sleep(random.uniform(0.5, 1.5)) 

    except KeyboardInterrupt:
        print("\nFlushing records and shutting down...")
    finally:
        producer.flush()

if __name__ == "__main__":
    main()
