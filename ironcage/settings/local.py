from .base import *  # flake8: noqa

DEBUG = bool(os.environ.get('DEBUG'))

ALLOWED_HOSTS = ['*']

# A custom setting for creating full URLs in links in emails
DOMAIN = 'http://localhost:8000'

# Password validators are a pain when testing locally
AUTH_PASSWORD_VALIDATORS = []

# Write emails to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Write Slack messages to the console
SLACK_BACKEND = 'django_slack.backends.ConsoleBackend'

# Don't log Slack error reports to the console
LOGGING['loggers']['django']['handlers'].remove('slack')

# Closing times
bst = timezone(timedelta(hours=1))
CFP_CLOSE_AT = datetime(2018, 6, 15, 12, 0, tzinfo=bst)
GRANT_APPLICATIONS_CLOSE_AT = datetime(2018, 6, 15, 12, 0, tzinfo=bst)
