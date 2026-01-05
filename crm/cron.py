from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE_HEARTBEAT = "/tmp/crm_heartbeat_log.txt"
LOG_FILE_LOW_STOCK = "/tmp/low_stock_updates_log.txt"

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

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

    with open(LOG_FILE_HEARTBEAT, "a") as f:
        f.write(f"{timestamp} CRM is alive - GraphQL response: {response_status}\n")


def update_low_stock():
    """
    Runs every 12 hours via django-crontab.
    Executes the GraphQL mutation 'updateLowStockProducts' and logs output.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql("""
    mutation {
        updateLowStockProducts {
            products {
                id
                name
                stock
            }
            message
        }
    }
    """)

    try:
        result = client.execute(mutation)
        updated_products = result["updateLowStockProducts"]["products"]
    except Exception:
        updated_products = []

    with open(LOG_FILE_LOW_STOCK, "a") as f:
        for product in updated_products:
            f.write(f"{timestamp} Product updated: {product['name']} New stock: {product['stock']}\n")
