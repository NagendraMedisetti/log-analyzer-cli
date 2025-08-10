import re
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LogParser:
    # Apache Common Log Format with referrer and user-agent
    LOG_PATTERN = re.compile(
        r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) - - \[(?P<timestamp>[^\]]+)\] '
        r'"(?P<method>\w+) (?P<path>[^"]+?) HTTP/[\d.]+" '
        r'(?P<status>\d{3}) (?P<bytes>\d+|-) "(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
    )

    def parse_line(self, line):
        match = self.LOG_PATTERN.match(line)
        if not match:
            logging.warning(f"Malformed log line: {line.strip()}")
            return None

        try:
            data = match.groupdict()

            # Convert types
            data["timestamp"] = datetime.strptime(data["timestamp"], "%d/%b/%Y:%H:%M:%S %z")
            data["status"] = int(data["status"])
            data["bytes"] = int(data["bytes"]) if data["bytes"].isdigit() else 0
            return data

        except Exception as e:
            logging.error(f"Error parsing line: {e}")
            return None
