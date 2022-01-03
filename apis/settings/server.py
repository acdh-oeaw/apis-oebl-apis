from .base import *
import os
import re
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "^mm-24*i-6iecm7c@z9l+7%^ns^4g^z!8=dgffg4ulggr-4=1%"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


DEV_VERSION = os.environ.get("APIS_DEV_VERSION", True)

INSTALLED_APPS += ["apis_highlighter", "corsheaders", "haystack", "theme", "leaflet", "sass_processor"]

CORS_ALLOWED_ORIGINS = ["https://sennierer.github.io"]

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.solr_backend.SolrEngine",
        "URL": f"http://{os.environ.get('APIS_HAYSTACK_URL', 'apissolr')}:8983/solr/{os.environ.get('APIS_HAYSTACK_CORE', 'apis_solr')}",
        "ADMIN_URL": f"http://{os.environ.get('APIS_HAYSTACK_URL', 'apissolr')}:8983/solr/admin/cores",
    }
}

ALLOWED_HOSTS = re.sub(
    r"https?://",
    "",
    os.environ.get(
        "ALLOWED_HOSTS", os.environ.get("GITLAB_ENVIRONMENT_URL", "localhost,127.0.0.1")
    ),
).split(",")
# You need to allow '10.0.0.0/8' for service health checks.

ALLOWED_CIDR_NETS = ["10.0.0.0/8", "127.0.0.0/8"]

REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = (
    "rest_framework.permissions.IsAuthenticated",
)

CSRF_TRUSTED_ORIGINS = ["apis-edits.acdh-dev.oeaw.ac.at"]

APIS_RELATIONS_FILTER_EXCLUDE += ["annotation", "annotation_set_relation"]

REDMINE_ID = "16111"

SPECTACULAR_SETTINGS["COMPONENT_SPLIT_REQUEST"] = True
SPECTACULAR_SETTINGS["COMPONENT_NO_READ_ONLY_REQUIRED"] = True

DATABASES = {}

DATABASES["default"] = dj_database_url.config(conn_max_age=600)

APIS_BASE_URI = "https://apis.acdh.oeaw.ac.at/"

APIS_SKOSMOS = {
    "url": os.environ.get("APIS_SKOSMOS", "https://vocabs.acdh-dev.oeaw.ac.at"),
    "vocabs-name": os.environ.get("APIS_SKOSMOS_THESAURUS", "apisthesaurus"),
    "description": "Thesaurus of the APIS project. Used to type entities and relations.",
}

APIS_BLAZEGRAPH = (
    os.environ.get(
        "APIS_TRIPLESTORE", "https://triplestore.acdh-dev.oeaw.ac.at/omnipot/sparql"
    ),
    os.environ.get("APIS_TRIPLESTORE_USERNAME", ""),
    os.environ.get("APIS_TRIPLESTORE_PASSWORD", ""),
)

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://52a791b36a6f459e8c8b801677ec304c@sentry.io/1882721",
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

SASS_ROOT = os.path.join(BASE_DIR, 'theme', 'static','theme', 'scss', 'fundament_oebl')

SASS_PROCESSOR_ROOT = SASS_ROOT

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)



PROJECT_NAME = "apis"
