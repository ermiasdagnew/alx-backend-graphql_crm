from datetime import datetime

def log_crm_heartbeat():
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        ts = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        f.write(f"{ts} CRM is alive\n")

def update_low_stock():
    with open("/tmp/low_stock_updates_log.txt", "a") as f:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{ts} Low stock update executed\n")
