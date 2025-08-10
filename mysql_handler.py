import mysql.connector
from configparser import ConfigParser
import logging

class MySQLHandler:
    def __init__(self, config_path="config.ini"):
        # Read DB config
        config = ConfigParser()
        config.read(config_path)
        db = config["mysql"]

        self.conn = mysql.connector.connect(
            host=db["host"],
            user=db["user"],
            password=db["password"],
            database=db["database"]
        )
        self.cursor = self.conn.cursor(dictionary=True)
        logging.info("Connected to MySQL")

    def create_tables(self):
        # Create user_agents and log_entries tables
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_agents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_agent_string VARCHAR(512) UNIQUE NOT NULL,
            os VARCHAR(100),
            browser VARCHAR(100),
            device_type VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS log_entries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ip_address VARCHAR(45) NOT NULL,
            timestamp DATETIME NOT NULL,
            method VARCHAR(10) NOT NULL,
            path VARCHAR(2048) NOT NULL,
            status_code SMALLINT NOT NULL,
            bytes_sent INT NOT NULL,
            referrer VARCHAR(2048),
            user_agent_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_agent_id) REFERENCES user_agents(id)
        )
        """)
        self.conn.commit()
        logging.info("Tables created")

    def _get_or_insert_user_agent(self, user_agent_string):
        self.cursor.execute("SELECT id FROM user_agents WHERE user_agent_string = %s", (user_agent_string,))
        result = self.cursor.fetchone()
        if result:
            return result["id"]

        # Simple parsing for OS, browser, device
        os = "Unknown"
        browser = "Unknown"
        device = "Desktop"

        if "Windows" in user_agent_string: os = "Windows"
        elif "Linux" in user_agent_string: os = "Linux"
        elif "Macintosh" in user_agent_string: os = "macOS"

        if "Chrome" in user_agent_string: browser = "Chrome"
        elif "Firefox" in user_agent_string: browser = "Firefox"
        elif "Safari" in user_agent_string: browser = "Safari"

        if "Mobile" in user_agent_string: device = "Mobile"
        elif "Tablet" in user_agent_string: device = "Tablet"

        self.cursor.execute("""
            INSERT INTO user_agents (user_agent_string, os, browser, device_type)
            VALUES (%s, %s, %s, %s)
        """, (user_agent_string, os, browser, device))
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_batch_log_entries(self, log_list):
        entries = []
        for log in log_list:
            user_agent_id = self._get_or_insert_user_agent(log["user_agent"])
            entries.append((
                log["ip"],
                log["timestamp"],
                log["method"],
                log["path"],
                log["status"],
                log["bytes"],
                log["referrer"],
                user_agent_id
            ))

        self.cursor.executemany("""
            INSERT INTO log_entries
            (ip_address, timestamp, method, path, status_code, bytes_sent, referrer, user_agent_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, entries)
        self.conn.commit()
        logging.info(f"Inserted {len(entries)} log entries")

    def get_top_n_ips(self, n):
        self.cursor.execute("""
            SELECT ip_address, COUNT(*) AS request_count
            FROM log_entries
            GROUP BY ip_address
            ORDER BY request_count DESC
            LIMIT %s
        """, (n,))
        return self.cursor.fetchall()

    def get_status_code_distribution(self):
        self.cursor.execute("""
            SELECT status_code, COUNT(*) AS count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM log_entries), 2) AS percentage
            FROM log_entries
            GROUP BY status_code
            ORDER BY count DESC
        """)
        return self.cursor.fetchall()

    def get_hourly_traffic(self):
        self.cursor.execute("""
            SELECT HOUR(timestamp) AS hour, COUNT(*) AS request_count
            FROM log_entries
            GROUP BY hour
            ORDER BY hour
        """)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
        logging.info("MySQL connection closed")

    