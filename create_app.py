import faust
import config

def create_app():
    app = faust.App(config.FAUST_APP_NAME, broker=config.KAFKA_BROKER_URL)

    return app