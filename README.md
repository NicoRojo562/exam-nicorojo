# exam-nicorojo

# Aviation Data ETL Pipeline

This project is an **ETL pipeline** built with **Apache Airflow**, **MySQL**, and **Python** to extract, transform, and load aviation flight data from the [AviationStack API](https://aviationstack.com/). The pipeline fetches flight data, processes it, and stores it in a MySQL database running inside a Docker container.

## Table of Contents
1. [Technologies Used](#technologies-used)
2. [Project Structure](#project-structure)
3. [How to Run the Project](#how-to-run-the-project)
   - [Running with Docker](#running-with-docker)
   - [Running Locally](#running-locally)
4. [Accessing Apache Airflow](#accessing-apache-airflow)
5. [Connecting to MySQL Database](#connecting-to-mysql-database)
6. [Viewing Data in Jupyter Notebook](#viewing-data-in-jupyter-notebook)
7. [Author](#author)

---

## Technologies Used
- **Apache Airflow** – Orchestration and scheduling of the ETL pipeline.
- **MySQL** – Storage for structured aviation data.
- **Python** – Data extraction and processing.
- **Pandas** – Data manipulation.
- **SQLAlchemy** – Database connectivity.
- **Docker** – Containerization for easy deployment.

---

## How to Run the Project

### Running with Docker
Ensure you have **Docker** and **Docker Compose** installed.

#### Step 1: Clone the repository
```sh
git clone https://github.com/NicoRojo562/exam-nicorojo.git
cd exam-nicorojo
```

#### Step 2: Set up environment variables
Create a `.env` file in the project root and add the following: (for the porpose of the exam .env file is already generated)
```sh
AVIATIONSTACK_API_KEY=your_api_key_here
```

#### Step 3: Build and start the containers
```sh
docker-compose up --build
```
This will start:
- A **MySQL database** on port **3307**
- An **Airflow instance** on port **8080**

---

### Running Locally (Without Docker)
If you prefer to run the project without Docker, follow these steps:

#### Step 1: Create a Python virtual environment
```sh
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```

#### Step 2: Install dependencies
```sh
pip install -r airflow/requirements.txt
```
💡 Note: If you want to update the list of requirements after installing new libraries, you can use the following command:
```sh
pip freeze > airflow/requirements.txt
```
This will generate an updated requirements.txt file for you.

#### Step 3: Set up MySQL database
Ensure you have MySQL running and create the database manually (FYI: DAG later will do it for you if you want to skip this step):
```sql
CREATE DATABASE testfligoo;
```

#### Step 4: Run the Airflow scheduler
```sh
airflow db init
airflow scheduler &
airflow webserver --port 8080
```

#### Step 5: Run the DAG manually
Go to the Airflow UI and **trigger** the **aviation_etl** DAG.

---

## Accessing Apache Airflow
Once the project is running, go to:

🔗 **http://localhost:8080**  


Default credentials are not that easy to find. Recomendation: create a new Airflow admin user, run:
```sh
airflow users create \
    --username admin2 \
    --firstname Nicolas \
    --lastname Rojo \
    --role Admin \
    --email yo@ex.com \
    --password admin
```

---

## Connecting to MySQL Database
You can connect to the MySQL database from your terminal:
```sh
mysql -h 127.0.0.1 -P 3307 -u root -p
```
OR in the container
```sh
docker exec -it mysql-db mysql -uroot -proot 
```
Then check if the data is loaded:
```sql
USE testfligoo;
SELECT * FROM testdata LIMIT 5;
```

---

## Viewing Data in Jupyter Notebook
To analyze the extracted data using **Jupyter Notebook**:

#### Step 1: Start Jupyter Notebook
```sh
jupyter notebook
```

#### Step 2: Connect to the MySQL Database
Inside a Jupyter Notebook cell, run:
```python
from sqlalchemy import create_engine
import pandas as pd

# Connect to MySQL in Docker
engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3307/testfligoo")

# Fetch data into a Pandas DataFrame
df = pd.read_sql("SELECT * FROM testdata", con=engine)
df.head()
```

---

## Author
📌 **Ingeniero Nicolas Rojo**  
🚀 **Data Engineer & Software Developer**
