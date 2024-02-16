#!/bin/bash

KAFKA_HOST=$1
KAFKA_PORT=$2
SCRIPT=$3

sleep 15

>&2 echo "Kafka is up - executing command"

faust -A app worker -l info

python3 $SCRIPT &

