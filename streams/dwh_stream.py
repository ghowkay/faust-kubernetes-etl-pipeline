from create_app import create_app
import config
from agents.metadata_agent import metadata_table
import json
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

app = create_app()

# Snowflake Connection
conn = snowflake.connector.connect(
    user= config.SNOWFLAKE_USER,
    password=config.SNOWFLAKE_PASSWORD,
    account=config.SNOWFLAKE_ACCOUNT,
    warehouse=config.SNOWFLAKE_WAREHOUSE,
    database=config.SNOWFLAKE_DATABASE
)

dwh_table = config.SNOWFLAKE_TABLE

BATCH_SIZE=100

# Define an empty DataFrame
df = pd.DataFrame()


async def process_dwh_stream(stream):
    global df
    data = []
    async for metrics_node_id, metrics_value in stream.items():
        # Logic to process and direct data to the DWH

        if metrics_node_id in metadata_table:

            instance_metadata = metadata_table[metrics_node_id]

            # Merge the two records
            flattened_record = {**json.loads(instance_metadata), **metrics_value}
            flattened_record.pop('node_id')  # Remove duplicate key

            #append to the DataFrame
            new_row = pd.DataFrame([flattened_record])
            df = pd.concat([df, new_row], ignore_index=True)

            # When DataFrame reaches batch size, write to Snowflake and reset
            if len(df) >= BATCH_SIZE:
                conn.cursor().execute(f"USE DATABASE {config.SNOWFLAKE_DATABASE}")
                success, nchunks, nrows, _ = write_pandas(conn, 
                                          df, 
                                          dwh_table, 
                                          chunk_size = 100, 
                                          schema = 'PUBLIC',
                                          auto_create_table=True
                                          )
                print(success)
                df = df[0:0]  # Reset DataFrame