import random
from datetime import datetime, timedelta

# Predefined values for random generation
methods = ["GET", "POST", "PUT", "DELETE"]
paths = ["/index.html", "/login", "/products", "/contact", "/about", "/services", "/search"]
statuses = [200, 201, 302, 400, 401, 403, 404, 500, 503]
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 11)"
]

def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def random_date():
    now = datetime.now()
    delta = timedelta(minutes=random.randint(0, 10000))
    return (now - delta).strftime("%d/%b/%Y:%H:%M:%S +0000")

# Generate 100 log entries
with open("sample_logs/fake_access.log", "w") as f:
    for _ in range(100):
        log_line = (
            f"{random_ip()} - - [{random_date()}] "
            f"\"{random.choice(methods)} {random.choice(paths)} HTTP/1.1\" "
            f"{random.choice(statuses)} {random.randint(100, 2000)} "
            f"\"-\" \"{random.choice(user_agents)}\""
        )
        f.write(log_line + "\n")

print("✅ 100 fake log entries written to sample_logs/fake_access.log")
