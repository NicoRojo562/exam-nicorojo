FROM apache/airflow:2.7.0-python3.10

# working directory
WORKDIR /opt/airflow

COPY airflow/requirements.txt requirements.txt
COPY airflow/dags dags/

#Install all dep
RUN pip install --no-cache-dir -r requirements.txt

ENV AIRFLOW_HOME=/opt/airflow

RUN airflow db init
EXPOSE 8080
CMD ["airflow", "standalone"]
