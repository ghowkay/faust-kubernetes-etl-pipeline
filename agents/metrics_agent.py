from create_app import create_app
from models.metrics import Metrics
import config

app = create_app()

dwh_topic = app.topic(config.DWH_STREAM_TOPIC)
ml_feature_topic = app.topic(config.ML_FEATURE_STREAM_TOPIC)

async def process_metrics(metrics_stream): 
    async for key, metric in metrics_stream.items():
        
        # Example of sending processed data to DWH stream
        await dwh_topic.send(key=key,value=metric)

        # Example of sending processed data to ML feature stream
        await ml_feature_topic.send(key=key,value=metric)
