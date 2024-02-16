import pandas as pd
from kafka import KafkaProducer
import json
import config
import pyarrow.parquet as pq
import threading

# Kafka Producer Configuration
producer = KafkaProducer(
    bootstrap_servers=[config.KAFKA_BROKER_URL],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
def send_metadata_data_to_topic(topic, df):

    for _, row in df.iterrows():

        record_value = row.to_dict()
        record_key = row.to_dict()['id']

        producer.send(topic, key=record_key.encode('utf-8'), value=record_value)


def send_metrics_data_to_topic(topic, df):

    df['created_at'] = df['created_at'].apply(lambda x: x.isoformat())

    for _, row in df.iterrows():

        record_value = row.to_dict()
        record_key = row.to_dict()['node_id']

        if record_key is not None:
       
            producer.send(topic, key=record_key.encode('utf-8'), value=record_value)

def load_and_send_data_in_batches(file_path, topic, type, batch_size=10000):
    parquet_file = pq.ParquetFile(file_path)
    for batch in parquet_file.iter_batches(batch_size=batch_size):
        df = batch.to_pandas()

        if type == 'metadata':
            send_metadata_data_to_topic(topic, df)

        if type == 'metrics':
            send_metrics_data_to_topic(topic, df)

if __name__ == "__main__":
    threading.Thread(target=load_and_send_data_in_batches, 
                              args=(config.NODE_METADATA_PARQUET_PATH, config.NODE_METADATA_TOPIC, 'metadata')).start()
    threading.Thread(target=load_and_send_data_in_batches, 
                               args=(config.METRICS_PARQUET_PATH, config.METRICS_TOPIC, 'metrics')).start()