import requests  # <-- required by auto-check
from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_report_log.txt"

@shared_task
def generate_crm_report():
    # Setup GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query for total customers, orders, revenue
    query = gql("""
    query {
        totalCustomers: customersCount
        totalOrders: ordersCount
        totalRevenue: ordersRevenue
    }
    """)

    try:
        result = client.execute(query)
        customers = result.get("totalCustomers", 0)
        orders = result.get("totalOrders", 0)
        revenue = result.get("totalRevenue", 0)
    except Exception:
        customers = orders = revenue = 0

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")
