```
# Log File Analysis & Reporting System

A Python-based CLI tool that processes web server log files, extracts structured data, stores it in a MySQL database, and generates insightful reports on web traffic patterns, user behavior, and server performance.

## Project Goals

- Convert unstructured Apache-style log files into structured data.
- Store structured data in a normalized MySQL database.
- Enable reporting on top IPs, most visited pages, status codes, and hourly traffic.
- Simulate a real-world Data Engineering workflow: Ingest → Transform → Store → Analyze.

## Tech Stack

| Component           | Technology |
|---------------------|------------|
| Programming Language| Python 3.x |
| Database            | MySQL 8.x  |
| CLI & Parsing       | argparse, re, datetime |
| DB Connector        | mysql-connector-python |
| Output Formatting   | tabulate |
| Config Management   | configparser |
| IDE/Editor          | VS Code    |

## Project Structure

```

log\_analyzer\_cli/
├── main.py               # CLI entry point
├── log\_parser.py         # Parses log entries
├── mysql\_handler.py      # Handles MySQL operations
├── generate\_logs.py      # Generates fake logs (optional)
├── config.ini            # DB config (not pushed to GitHub)
├── sample\_logs/          # Sample log files
│   ├── access.log
│   └── fake\_access.log
├── sql/
│   └── create\_tables.sql # MySQL table schema
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── .gitignore            # Files ignored from Git

````

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/log-analyzer-cli.git
cd log-analyzer-cli
````

### 2. Create & activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL connection

Edit `config.ini` (not pushed to GitHub):

```ini
[mysql]
host = localhost
user = root
password = your_password
database = weblogs_db
```

## Generating Fake Logs (Optional)

```bash
python generate_logs.py
```

Generates `fake_access.log` in `sample_logs/`.

## Processing Logs

```bash
python main.py process_logs sample_logs/access.log --batch_size 100
```

* Reads the log file
* Parses valid lines
* Inserts data into MySQL in batches

## Generating Reports

### Top IP addresses

```bash
python main.py generate_report top_n_ips --value 5
```

### Top visited pages

```bash
python main.py generate_report top_n_pages --value 5
```

### Hourly traffic

```bash
python main.py generate_report hourly_traffic
```

### Status code distribution

```bash
python main.py generate_report status_code_distribution
```

## Database Schema

### Table: `log_entries`

| Field           | Type     | Description            |
| --------------- | -------- | ---------------------- |
| id              | INT PK   | Unique log ID          |
| ip\_address     | VARCHAR  | Source IP address      |
| timestamp       | DATETIME | Request time           |
| method          | VARCHAR  | HTTP method            |
| path            | VARCHAR  | Requested URL          |
| status\_code    | INT      | HTTP status code       |
| bytes\_sent     | INT      | Size of response       |
| referrer        | VARCHAR  | Referrer URL           |
| user\_agent\_id | INT FK   | Links to `user_agents` |

### Table: `user_agents`

| Field               | Type    | Description      |
| ------------------- | ------- | ---------------- |
| id                  | INT PK  | Unique ID        |
| user\_agent\_string | VARCHAR | Full UA string   |
| os                  | VARCHAR | Operating System |
| browser             | VARCHAR | Browser name     |
| device\_type        | VARCHAR | Device type      |

## Learning Outcomes

* Parsing semi-structured log data using regex
* Designing relational database schemas
* Batch insertion into MySQL
* Creating SQL-based analytical reports
* Building CLI tools with Python

```

```
