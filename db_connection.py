import psycopg2
from psycopg2 import pool

class PostgresDB:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'postgres',
            'user': 'postgres',
            'password': 'postgreS@1234'
        }
        self.connection_pool = None
        self.init_connection_pool()

    def init_connection_pool(self):
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 10,  # Min 1, Max 10 connections in pool
                **self.db_config
            )
            print(" PostgreSQL connection pool created successfully")
        except Exception as e:
            print(" Error creating connection pool:", e)

    def get_connection(self):
        try:
            if self.connection_pool:
                return self.connection_pool.getconn()
        except Exception as e:
            print(" Error getting connection:", e)

    def return_connection(self, connection):
        try:
            if self.connection_pool:
                self.connection_pool.putconn(connection)
        except Exception as e:
            print("❌ Error returning connection to pool:", e)

    def close_all_connections(self):
        if self.connection_pool:
            self.connection_pool.closeall()
            print("All connections closed")
