import sqlite3
import os

def check_database():
    if os.path.exists('shop.db'):
        print("✓ Database file exists")
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("Database tables:")
        for table in tables:
            print(f"  ✓ {table[0]}")
        conn.close()
    else:
        print("✗ Database file not found")

if __name__ == "__main__":
    check_database()