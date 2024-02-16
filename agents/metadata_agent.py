from create_app import create_app
from models.node_metadata import NodeMetadata
import config
import json

app = create_app()

metadata_table = app.Table('metadata_table', default=str)

dwh_topic = app.topic(config.DWH_STREAM_TOPIC)
ml_feature_topic = app.topic(config.ML_FEATURE_STREAM_TOPIC)

async def process_node_metadata(metadata_stream):
    async for key, value in metadata_stream.items():
        
        metadata_table[key] = json.dumps(value)

