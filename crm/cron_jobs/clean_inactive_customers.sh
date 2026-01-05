#!/bin/bash

PROJECT_DIR="/path/to/alx-backend-graphql_crm"
PYTHON="/path/to/venv/bin/python"
MANAGE="$PROJECT_DIR/manage.py"
LOG_FILE="/tmp/customer_cleanup_log.txt"

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

DELETED_CUSTOMERS=$(
$PYTHON $MANAGE shell <<EOF
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

# Customers inactive for 365 days
inactive_date = timezone.now() - timedelta(days=365)

qs = Customer.objects.filter(orders__isnull=True, created_at__lt=inactive_date)

count = qs.count()
qs.delete()

print(count)
EOF
)

echo "$TIMESTAMP Deleted customers: $DELETED_CUSTOMERS" >> $LOG_FILE
