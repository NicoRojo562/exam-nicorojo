import mysql.connector
import os
from scripts.fetch_data import fetch_flights

DB_CONFIG = {
    "host": "mysql-db",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "testfligoo"
}

def create_database():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        conn.commit()
        print(f"Base de datos `{DB_CONFIG['database']}` verificada/creada en MySQL")
    except mysql.connector.Error as e:
        print(f"Error creando la base de datos: {e}")
    finally:
        conn.close()

def create_table():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS testdata (
                id INT AUTO_INCREMENT PRIMARY KEY,
                flight_date DATE,
                flight_status VARCHAR(20),
                departure_airport VARCHAR(100),
                departure_timezone VARCHAR(50),
                arrival_airport VARCHAR(100),
                arrival_timezone VARCHAR(50),
                arrival_terminal VARCHAR(50),
                airline_name VARCHAR(100),
                flight_number VARCHAR(20)
            );
        """)
        conn.commit()
        print("Tabla `testdata` verificada/creada en MySQL")
    except mysql.connector.Error as e:
        print(f"Error en MySQL: {e}")
    finally:
        conn.close()

def insert_data():
    conn = None
    try:
        df = fetch_flights()
        if df.empty:
            print("⚠️ No hay datos para insertar.")
            return

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        data_tuples = [tuple(row) for row in df.itertuples(index=False, name=None)]

        query = """
            INSERT INTO testdata (
                flight_date, flight_status, departure_airport, departure_timezone,
                arrival_airport, arrival_timezone, arrival_terminal, airline_name, flight_number
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(query, data_tuples) #all inserts in one op
        conn.commit()
        print(f"Insertadas {len(df)} filas en MySQL")

    except mysql.connector.Error as e:
        print(f"Error en MySQL: {e}")

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_database()
    create_table()     
    insert_data()     
