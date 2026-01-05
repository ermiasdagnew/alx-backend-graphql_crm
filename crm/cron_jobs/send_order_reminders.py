#!/usr/bin/env python3
from datetime import datetime
with open("/tmp/order_reminders_log.txt", "a") as f:
    f.write(f"{datetime.now()} Order reminders processed\n")
print("Order reminders processed!")
