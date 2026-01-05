INSTALLED_APPS = [
    # default Django apps...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # your apps
    'crm',

    # Cron and Celery apps
    'django_crontab',        # <-- must be literally like this
    'django_celery_beat',
]

# ========================
# django-crontab jobs
# ========================
CRONJOBS = [
    # Heartbeat every 5 minutes
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
    # Low stock updates every 12 hours
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]

# ========================
# Celery configuration
# ========================
CELERY_BROKER_URL = 'redis://localhost:6379/0'

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}
