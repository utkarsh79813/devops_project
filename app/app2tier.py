from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME","testdb"),
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def health():
    return jsonify ({"status":"App is running"}), 200

@app.route("/db")
def db_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()    # Creates a cursor object. use to Execute SQL commands

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50)
                )
        """)

        cursor.execute("INSERT INTO users (name) VALUES ('DevOps User')")
        conn.commit()

        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify ({
            "message": "Connected to MySQL successfully",
            "data": rows
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)