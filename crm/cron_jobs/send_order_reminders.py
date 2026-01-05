#!/usr/bin/env python3

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/order_reminders_log.txt"

# GraphQL client setup
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(
    transport=transport,
    fetch_schema_from_transport=True
)

# GraphQL query for recent orders
query = gql("""
query GetRecentOrders($since: DateTime!) {
  orders(orderDate_Gte: $since) {
    id
    customer {
      email
    }
  }
}
""")

since = (datetime.utcnow() - timedelta(days=7)).isoformat()

result = client.execute(
    query,
    variable_values={"since": since}
)

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(LOG_FILE, "a") as log:
    for order in result.get("orders", []):
        log.write(
            f"{timestamp} Order ID: {order['id']} Email: {order['customer']['email']}\n"
        )

print("Order reminders processed!")
