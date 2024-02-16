# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

RUN pip install pandas
RUN pip install pyarrow
RUN pip install snowflake-connector-python
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Define environment variable
ENV NAME DataPipelineApp