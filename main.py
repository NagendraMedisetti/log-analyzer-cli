import argparse
import logging
from log_parser import LogParser
from mysql_handler import MySQLHandler
from tabulate import tabulate

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def process_logs(file_path, batch_size):
    parser = LogParser()
    db = MySQLHandler()
    db.create_tables()

    batch = []
    total = 0

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            parsed = parser.parse_line(line)
            if parsed:
                batch.append(parsed)

            if len(batch) >= batch_size:
                db.insert_batch_log_entries(batch)
                total += len(batch)
                batch = []

    if batch:
        db.insert_batch_log_entries(batch)
        total += len(batch)

    logging.info(f"Finished processing {total} log entries")
    db.close()

def generate_report(report_type, value=None):
    db = MySQLHandler()

    try:
        if report_type == "top_n_ips":
            result = db.get_top_n_ips(value or 5)
            print(tabulate(result, headers="keys", tablefmt="grid"))

        elif report_type == "status_code_distribution":
            result = db.get_status_code_distribution()
            print(tabulate(result, headers="keys", tablefmt="grid"))

        elif report_type == "hourly_traffic":
            result = db.get_hourly_traffic()
            print(tabulate(result, headers="keys", tablefmt="grid"))

        elif report_type == "top_n_pages":
            db.cursor.execute("""
                SELECT path, COUNT(*) AS request_count
                FROM log_entries
                GROUP BY path
                ORDER BY request_count DESC
                LIMIT %s
            """, (value or 5,))
            result = db.cursor.fetchall()
            print(tabulate(result, headers="keys", tablefmt="grid"))

        else:
            print("Unsupported report type.")

    except Exception as e:
        print("Error generating report:", e)

    finally:
        db.close()

def main():
    parser = argparse.ArgumentParser(description="Log File Analysis & Reporting System")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # process_logs command
    process_cmd = subparsers.add_parser("process_logs", help="Process a log file")
    process_cmd.add_argument("file_path", type=str, help="Path to the log file")
    process_cmd.add_argument("--batch_size", type=int, default=500, help="Batch size for DB inserts")

    # generate_report command
    report_cmd = subparsers.add_parser("generate_report", help="Generate report")
    report_cmd.add_argument("report_type", choices=["top_n_ips", "status_code_distribution", "hourly_traffic", "top_n_pages"], help="Report type")
    report_cmd.add_argument("--value", type=int, help="Optional value (e.g., N for top N IPs)")

    args = parser.parse_args()

    if args.command == "process_logs":
        process_logs(args.file_path, args.batch_size)
    elif args.command == "generate_report":
        generate_report(args.report_type, args.value)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
