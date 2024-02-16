from create_app import create_app
import config
from agents.metrics_agent import process_metrics
from agents.metadata_agent import process_node_metadata
from streams.dwh_stream import process_dwh_stream
from streams.ml_stream import process_ml_stream

# Initialize the Faust app
app = create_app()

# Define Kafka topics
metrics_topic = app.topic(config.METRICS_TOPIC)
node_metadata_topic = app.topic(config.NODE_METADATA_TOPIC)
dwh_topic = app.topic(config.DWH_STREAM_TOPIC)
ml_feature_topic = app.topic(config.ML_FEATURE_STREAM_TOPIC)

# Link agents to topics
metadata_agent = app.agent(node_metadata_topic)(process_node_metadata)
metrics_agent = app.agent(metrics_topic)(process_metrics)

# Define stream processors
dwh_stream_processor = app.agent(dwh_topic)(process_dwh_stream)
ml_stream_processor = app.agent(ml_feature_topic)(process_ml_stream)

if __name__ == '__main__':

    app.main()