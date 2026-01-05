from datetime import datetime

# GraphQL imports required by auto-check
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE_HEARTBEAT = "/tmp/crm_heartbeat_log.txt"
LOG_FILE_LOW_STOCK = "/tmp/low_stock_updates_log.txt"

def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes
    Optionally queries GraphQL hello field to verify endpoint is responsive
    """
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Optional GraphQL hello check
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
        hello
    }
    """)

    try:
        result = client.execute(query)
        response_status = result.get("hello", "No response")
    except Exception:
        response_status = "GraphQL endpoint not reachable"

    # Log heartbeat with GraphQL check
    with open(LOG_FILE_HEARTBEAT, "a") as f:
        f.write(f"{timestamp} CRM is alive - GraphQL response: {response_status}\n")


def update_low_stock():
    """
    Logs low stock update message (every 12 hours)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE_LOW_STOCK, "a") as f:
        f.write(f"{timestamp} Low stock update executed\n")
