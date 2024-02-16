# Kubernetes Metrics Processing Application

## Overview
This application processes Kubernetes workload resource utilization metrics. It's built with Faust, Kafka, and Docker, focusing on real-time data processing and transformation for Data Warehouse optimization and Machine Learning model preparation.

## Pipeline Description
This application's pipeline follows these steps:

1. **Data Ingestion**: Kubernetes Data is ingested from the datasets provided detailing workload resource utilization metrics. We can also assume data is ingested from kubernetes directly

2. **Kafka Streaming**: The ingested data is streamed through Kafka, serving as the backbone for real-time data processing.

3. **Faust Processing**: Faust workers process the streaming data, performing tasks such as:
   - Aggregating metrics and Transforming data for ML model readiness
   - Preparing data for efficient querying in a Data Warehouse setup - (Snowflake)

4. **Docker-Compose Orchestration**: All components, including Kafka brokers, Zookeeper, and Faust workers, are containerized and managed using Docker-compose, ensuring streamlined deployment and scalability.

Each component is configured to work harmoniously, ensuring efficient data flow from ingestion to processing.


## Key Components

### `models/`
- **Purpose**: Define the structure of data that the pipeline will process.
- **Contents**:
  - `metrics.py`: Defines the schema for metrics data.
  - `node_metadata.py`: Defines the schema for node metadata.

### `agents/`
- **Purpose**: Contain Faust agents that subscribe to Kafka topics and process incoming data streams.
- **Contents**:
  - `metrics_agent.py`: Processes incoming metrics data and sends to dwh and ml streams
  - `metadata_agent.py`: Processes incoming node metadata, creates a kakfa table on the the data to be used in the dwh
  and ml streams to join the metrics data

### `streams/`
- **Purpose**: Handle different data streams for specific purposes like Data Warehouse storage or ML feature transformation.
- **Contents**:
  - `dwh_stream.py`: Processes and directs data to the DWH stream.
  - `ml_stream.py`: Processes data for ML feature transformation.

### `app.py`
- **Purpose**: Initializes and configures the main Faust application. It sets up Kafka topics and links agents to these topics.

### `config.py`
- **Purpose**: Centralize configuration settings like Kafka broker URLs and topic names.

### `data_extraction.py`
- **Purpose**: Read the datasets from files and pushes to the kafka topics to be proceessed downstream


## Additional Notes
- Ensure that Kafka and Zookeeper are running and properly configured before starting the Faust application.
- The application is designed to be scalable and modular, allowing for easy additions and modifications to data models and stream processors.


## Getting Started
Follow the installation and running instructions above to set up and start the application.

## Prerequisites
- Docker and Docker-compose
- Kafka
- Python 3.x
- Snowflake (Configure your snowflake accoun in the `config.py` file)


## Usage
The application processes data from Kafka topics, storing in snowflake as DWH and transforming it for various downstream applications (ML Feature store).



## Installation

```bash
  git clone https://github.com/ghowkay/faust-kubernetes-etl-pipeline.git
  cd faust-kubernetes-etl-pipeline
```

## Running the Application
Start the services with Docker-compose:

`docker-compose up --build -d`

## View the application logs
`docker-compose logs -f data-pipeline-app`

## Stopping the Application
To stop the application, run:

`docker-compose down`

## Note
Ic can take 10 - 15 minutes for the logs of the ml stream and dwh stream to be logged .This is due to the size of the data as well as resources on the machine

## View data in Snowflake

Once the pipeline is finished, you can view and query your data in your snowflake instance that is setup in the `config.py`