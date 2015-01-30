from settings import *

PRODUCTION = True
BUGSNAG['release_stage'] = "production"

import dj_database_url

DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}
