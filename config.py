# Kafka Configuration
KAFKA_BROKER_URL = 'kafka:9092'

# Kafka Topics
METRICS_TOPIC = 'metrics_topic'
NODE_METADATA_TOPIC = 'node_metadata_topic'
DWH_STREAM_TOPIC = 'dwh_stream_topic'
ML_FEATURE_STREAM_TOPIC = 'ml_feature_stream_topic'

# File Paths
METRICS_PARQUET_PATH = 'dataset/metrics.parquet.gz'
NODE_METADATA_PARQUET_PATH = 'dataset/node_metadata.parquet.gz'

# Faust App Configuration
FAUST_APP_NAME = 'data_pipeline_app'

#snowflake
'''
Configure snowflake credentials below before running application if you want to view and analyze data in warehouse
'''
SNOWFLAKE_TABLE='kube_node_metrics'
SNOWFLAKE_USER='USERNAME'
SNOWFLAKE_PASSWORD='PASSWORD'
SNOWFLAKE_ACCOUNT='ACCOUNT'
SNOWFLAKE_WAREHOUSE= 'WAREHOUSE'
SNOWFLAKE_DATABASE='DATABASE'
