import os
import socket
import time

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", 5432))

print(f"Waiting for database at {DB_HOST}:{DB_PORT}...")

while True:
    try:
        with socket.create_connection((DB_HOST, DB_PORT), timeout=2):
            print("Database is reachable.")
            break
    except OSError:
        time.sleep(1)