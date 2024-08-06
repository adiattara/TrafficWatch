FROM python:3.10-slim

RUN mkdir -p /opt/dagster/dagster_home

COPY requirements.txt /opt/dagster/dagster_home/

RUN cd /opt/dagster/dagster_home/ &&  pip install -r requirements.txt

# Copy your code and workspace to /opt/dagster/app
COPY workspace.yaml /opt/dagster/dagster_home/

# Copy dagster instance YAML to $DAGSTER_HOME
COPY dagster.yaml /opt/dagster/dagster_home/

COPY dagster_code/* /opt/dagster/dagster_home/dagster_code/

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

WORKDIR /opt/dagster/dagster_home