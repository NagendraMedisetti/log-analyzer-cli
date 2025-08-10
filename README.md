
---

# Log File Analysis & Reporting System

## Overview

The Log File Analysis & Reporting System is a Python-based CLI tool that processes web server log files, parses structured data, stores it in a MySQL database, and generates reports on traffic patterns, user behavior, and server performance.

It supports both real log ingestion and fake log generation for testing, with report outputs directly in the terminal.

## Objectives

* Parse unstructured web server logs into structured records.
* Store parsed data in a normalized MySQL schema.
* Generate insights via CLI commands.
* Support test log generation for simulation.
* Maintain configuration separately for security.

## Project Structure

```
log_analyzer_cli/
├── __pycache__/               # Python cache files
├── sample_logs/               # Raw log data samples
│   ├── access.log
│   └── fake_access.log
├── screenshots/               # CLI output screenshots
│   ├── generate_report_hourly.png
│   ├── generate_report_status.png
│   ├── generate_report_top_ips.png
│   └── generate_report_top_pages.png
├── sql/
│   └── create_tables.sql      # MySQL table schema
├── venv/                      # Virtual environment
├── .gitignore                 # Ignore rules for Git
├── config_template.ini        # Template for DB configuration
├── config.ini                 # Actual DB config (ignored in Git)
├── generate_logs.py           # Generates fake log entries
├── log_parser.py              # Parses log entries into structured data
├── main.py                    # CLI entry point
├── mysql_handler.py           # MySQL operations (connect, insert, query)
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
└── Log File Analysis....pptx  # Project presentation
```

## Tech Stack

| Component            | Technology             |
| -------------------- | ---------------------- |
| Programming Language | Python 3.x             |
| Database             | MySQL 8.x              |
| CLI & Parsing        | argparse, re, datetime |
| DB Connector         | mysql-connector-python |
| Output Formatting    | tabulate               |
| Config Management    | configparser           |
| IDE/Editor           | VS Code                |

## Database Schema

### `log_entries`

| Field           | Type     | Description           |
| --------------- | -------- | --------------------- |
| id              | INT PK   | Unique log ID         |
| ip\_address     | VARCHAR  | Source IP             |
| timestamp       | DATETIME | Request time          |
| method          | VARCHAR  | HTTP method           |
| path            | VARCHAR  | Requested URL         |
| status\_code    | INT      | HTTP status code      |
| bytes\_sent     | INT      | Size of response      |
| referrer        | VARCHAR  | Referrer URL          |
| user\_agent\_id | INT FK   | Links to user\_agents |

### `user_agents`

| Field               | Type    | Description      |
| ------------------- | ------- | ---------------- |
| id                  | INT PK  | Unique ID        |
| user\_agent\_string | VARCHAR | Full UA string   |
| os                  | VARCHAR | Operating System |
| browser             | VARCHAR | Browser name     |
| device\_type        | VARCHAR | Device type      |

## CLI Workflow

1. **Log Source** – Take input from `sample_logs/` or generated logs.
2. **Parsing** – `log_parser.py` uses regex to extract fields.
3. **Database Handling** – `mysql_handler.py` connects to MySQL, creates tables, and inserts batches.
4. **Reporting** – `main.py` triggers SQL queries and displays results with `tabulate`.

## Example Commands

* Process logs:

  ```bash
  python main.py process_logs sample_logs/access.log --batch_size 100
  ```
* Generate report (top pages):

  ```bash
  python main.py generate_report top_n_pages --value 5
  ```
* Hourly traffic:

  ```bash
  python main.py generate_report hourly_traffic
  ```

---

