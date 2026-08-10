DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
EXTERNAL_APPS = [
    'phonenumber_field',
]
LOCAL_APPS = [
    'apps.accounts.apps.AccountsConfig',
]

INSTALLED_APPS = DEFAULT_APPS + EXTERNAL_APPS + LOCAL_APPS
