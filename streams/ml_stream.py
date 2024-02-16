from create_app import create_app
import config
from datetime import timedelta
import json
from agents.metadata_agent import metadata_table
from models.average_calculation import AverageCalculation


app = create_app()

async def on_window_close(key, value):
   
    # Compute the ratio here
   max_cpu_usage_2_hour_prior_last_hour_ratio = calculate_max_cpu_usage_2_hour_prior_last_hour_ratio(key)
   avg_cpu_usage_2_hour_prior_last_hour_ratio = calculate_avg_cpu_usage_2_hour_prior_last_hour_ratio(key)

   max_cpu_last_hour = value if key in max_cpu_last_hour_table else None
   avg_cpu_last_hour =  value if key in avg_cpu_usage_last_hour_table else None
   max_cpu_2_hours_prior = value if key in max_cpu_2_hours_prior_table else None
   avg_cpu_2_hours_prior = value if key in avg_cpu_2_hours_prior_table else None
    
   # send the transformation data to feature store hypothetically here
   send_to_feature_store(max_cpu_usage_2_hour_prior_last_hour_ratio,
                         avg_cpu_usage_2_hour_prior_last_hour_ratio,
                         max_cpu_last_hour,
                         avg_cpu_last_hour['average'],
                         max_cpu_2_hours_prior,
                         avg_cpu_2_hours_prior['average'])


max_cpu_last_hour_table = app.Table(
    'max_cpu_last_hour', 
    default=int,
    on_window_close=on_window_close
    ).hopping(
        size=timedelta(hours=1), 
        step=timedelta(minutes=10), 
        expires=timedelta(hours=1)
        )

avg_cpu_usage_last_hour_table = app.Table(
    'avg_cpu_last_hour', 
    default=AverageCalculation,
    on_window_close=on_window_close
    ).hopping(
        size=timedelta(hours=1), 
        step=timedelta(minutes=10), 
        expires=timedelta(hours=1)
        )

max_cpu_2_hours_prior_table = app.Table(
    'max_cpu_2_hours_prior',
    default=int,
    on_window_close=on_window_close
).hopping(
    size=timedelta(hours=2),
    step=timedelta(minutes=10),
    expires=timedelta(hours=2)
)

avg_cpu_2_hours_prior_table = app.Table(
    'avg_cpu_2_hours_prior',
    default=AverageCalculation,
    on_window_close=on_window_close
).hopping(
    size=timedelta(hours=2),
    step=timedelta(minutes=10),
    expires=timedelta(hours=2)
)

   
def send_to_feature_store(*args):

    pass

async def process_ml_stream(stream):
    async for metrics_node_id, metrics_value in stream.items():
        # Logic to process and direct data to the DWH

        if metrics_node_id in metadata_table:

            instance_metadata = metadata_table[metrics_node_id]

            # Merge the two records
            flattened_record = {**json.loads(instance_metadata), **metrics_value}
            flattened_record.pop('node_id')  # Remove duplicate key

   
            cpu_usage = int(metrics_value['value'])

            # run calculations
            calculate_max_cpu_usage_last_hour(metrics_node_id, cpu_usage)
            calculate_avg_cpu_usage_last_hour(metrics_node_id, cpu_usage)
            calculate_max_cpu_usage_2_hours_prior(metrics_node_id, cpu_usage)
            calculate_avg_cpu_usage_2_hours_prior(metrics_node_id, cpu_usage)




# Metric Calculation Functions
def calculate_max_cpu_usage_last_hour(metrics_node_id,cpu_usage):

    current_max = max_cpu_last_hour_table[metrics_node_id].current()

    value = max(current_max, cpu_usage)
    max_cpu_last_hour_table[metrics_node_id] = value

    print(f"current max_cpu_usage_last_hour {value}")

    return value

def calculate_avg_cpu_usage_last_hour(metrics_node_id,cpu_usage):

    current_entry = avg_cpu_usage_last_hour_table[metrics_node_id].value()

    if current_entry is None:
        # If there's no entry yet, initialize total and count
        total = cpu_usage
        count = 1
    else:
        # If an entry exists, update total and count
        total = current_entry.total + cpu_usage
        count = current_entry.count + 1

    # Calculate the average
    average = total / count

    # Create a new instance of AverageCalculation with updated values
    new_entry = AverageCalculation(total=total, count=count, average=average)

    # Update the table with the new entry
    avg_cpu_usage_last_hour_table[metrics_node_id] = new_entry

    print(f"current avg_cpu_usage_last_hour: {average}")

    return average


def calculate_max_cpu_usage_2_hours_prior(metrics_node_id,cpu_usage):
    current_max = max_cpu_2_hours_prior_table[metrics_node_id].value()
    if current_max is None or cpu_usage > current_max:
        max_cpu_2_hours_prior_table[metrics_node_id] = cpu_usage

    return max_cpu_2_hours_prior_table[metrics_node_id]

def calculate_avg_cpu_usage_2_hours_prior(metrics_node_id,cpu_usage):
    current_entry = avg_cpu_2_hours_prior_table[metrics_node_id].value()

    if current_entry is None:
        # If there's no entry yet, initialize total and count
        total = cpu_usage
        count = 1
    else:
        # If an entry exists, update total and count
        total = current_entry.total + cpu_usage
        count = current_entry.count + 1

    # Calculate the average
    average = total / count

    # Create a new instance of AverageCalculation with updated values
    new_entry = AverageCalculation(total=total, count=count, average=average)

    # Update the table with the new entry
    avg_cpu_2_hours_prior_table[metrics_node_id] = new_entry

    print(f"current avg_cpu_usage_2_hours_prior: {average}")

    return average


def calculate_max_cpu_usage_2_hour_prior_last_hour_ratio(key):
    ratio = None
    if key in max_cpu_last_hour_table and key in max_cpu_2_hours_prior_table:
        last_hour_max = max_cpu_last_hour_table[key].value()
        two_hour_prior_max = max_cpu_2_hours_prior_table[key].value()
        if two_hour_prior_max != 0:
            ratio = last_hour_max / two_hour_prior_max

    print(f"max_cpu_usage_2_hour_prior_last_hour_ratio: {ratio}")

    return ratio


def calculate_avg_cpu_usage_2_hour_prior_last_hour_ratio(key):
    ratio = None
    if key in avg_cpu_usage_last_hour_table and key in avg_cpu_2_hours_prior_table:
        last_hour_avg = avg_cpu_usage_last_hour_table[key].value()['average']
        two_hour_prior_avg = avg_cpu_2_hours_prior_table[key].value()['average']
        if two_hour_prior_avg != 0:
            ratio = last_hour_avg / two_hour_prior_avg

    print(f"avg_cpu_usage_2_hour_prior_last_hour_ratio: {ratio}")

    return ratio

    