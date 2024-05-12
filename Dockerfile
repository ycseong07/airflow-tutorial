FROM apache/airflow:latest-python3.12
USER root

RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

USER airflow

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/home/airflow/.local/lib/python3.12/site-packages"
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/plugins"
