# -*- coding: utf-8 -*-
# Django settings for eracks11 project.

import sys
import os.path

# now set in local settings 1/3/13 jjW
DEBUG = True

ADMINS = (
    ('Joe', 'joe@eracks.com'),
)

MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = 'support@eracks.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL


PROJECT_ROOT = os.path.abspath(os.path.dirname (os.path.dirname(__file__)))

# for DjDT - 12/27/14 - test, still needed? JJW:
DATABASE_ENGINE = 'django.db.backends.postgresql_psycopg2'
USERENA_PROFILE_DETAIL_TEMPLATE = "%s/apps/home/templates/profile_detail.html" % PROJECT_ROOT

# This is the default, no? - JJW
#TEST_RUNNER = 'django.test.runner.DiscoverRunner'


# moved to local_settings 6/30/11 JJW
#DATABASES = dict (
#    default = dict (
#        ENGINE = 'django.db.backends.postgresql_psycopg2',        #, 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        NAME = 'eracksdb',             # Or path to database file if using sqlite3.
#        USER = 'eracks',             # Not used with sqlite3.
#        PASSWORD = 'Wav3lets9',         # Not used with sqlite3.
#        # HOST = 'eracks.com',             # Set to empty string for localhost. Not used with sqlite3.
#        # PORT = '5432',             # Set to empty string for default. Not used with sqlite3.
#        HOST = '127.0.0.1',             # Set to empty string for localhost. Not used with sqlite3.
#        PORT = '65432',             # Set to empty string for default. Not used with sqlite3.
#    )
#)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join (PROJECT_ROOT, 'media')


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = '/'  can't set this to /, django_filer requires reflexive media_root & urls, respectively
MEDIA_URL = '/media/'

# JJW 3/12
# nope - can't set to '', it thinks it's not set!
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join (PROJECT_ROOT, 'static')

STATICFILES_DIRS = (
    ('codemirror2', os.path.join (PROJECT_ROOT, 'packages/codemirror2')),
    ('js', os.path.join (PROJECT_ROOT, 'packages/aloha')),
    ('ckeditor', os.path.join (PROJECT_ROOT, 'packages/ckeditor')),
    os.path.join (PROJECT_ROOT, 'packages/foundation'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',  # JJW 11/9/15
)
GRAPPELLI_ADMIN_TITLE = "eRacks Administration"

GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a trailing slash.
# Examples: "http://foo.com/media/", "/media/".
# NOTE 5/27/12 JJW:  Even though this setting is not necessary for Django after staticfiles (and causes a deprecation warning), filebrowser still needs it
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3ad-v7@v!ho^c0((bhis%6)c*vvx55lorsn*55)8#9(on850wix'

# List of callables that know how to import templates from various sources.
if DEBUG:
  TEMPLATE_LOADERS = (  # these 2 are the default:
    'django.template.loaders.filesystem.Loader',  # load_template_source',
    'django.template.loaders.app_directories.Loader',  # load_template_source',
  #     'django.template.loaders.eggs.load_template_source',
  )
else:  # cache them
  TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
  )

MIDDLEWARE_CLASSES = (
    'stheme.middleware.ThemeLocalRequestMiddleware',
    'django.middleware.common.CommonMiddleware', # moved after redirect, 10/22/13 JJW
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'utils.middleware.SSLRedirectMiddleware',           # JJW 9/29/13
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    #'themes.middleware.ThemesMiddleware',
    #'django.middleware.common.CommonMiddleware', # nope didn't help 10/22/13 JJW
    # Common redirects in the request, redirectfallback in the response - so append-slash always preempts -
    # https://github.com/django/django/commit/64623a2e115d781c99c7df4dbb67a1e576c0165a
    # but even that was broken, so I had to fix it - see my middleware.py
    #'django.middleware.transaction.TransactionMiddleware',
)


# New for 1.8 - TEMPLATES dict

TEMPLATES = [
    dict (
        BACKEND = 'django.template.backends.django.DjangoTemplates',
        DIRS = [os.path.join (PROJECT_ROOT, 'templates'),],
        APP_DIRS = False,  # True, # do it manually co we can cotrol the order - see loaders= below
        OPTIONS = dict (
            context_processors = (
                # always on:
                #'django.template.context_processors.csrf',
                # defaults for 1.8
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # local django adds:
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                # local project adds:
                "utils.context_processors.settings",                    # JJW 4/2/12
                "utils.context_processors.models",                      # JJW 4/2/12
                "quickpages.context_processors.quick_snippets",         # JJW 11/7/15
                "quickpages.context_processors.quick_snippet_tags",     # JJW 11/7/15
                "home.context_processors.registration_forms",           # JJW 4/22/12
                "home.context_processors.cart_variables",               # JJW 6/10/12
                "home.context_processors.environment",                  # JJW 9/29/13
                "home.context_processors.google_analytics_tags",        # JJW 11/13/15
            ),
            loaders = (
              'stheme.template_loader.Loader',  # loads by theme
              'django.template.loaders.filesystem.Loader',
              'django.template.loaders.app_directories.Loader',
              #'django.template.loaders.eggs.load_template_source',
              #'dbtemplates.loader.Loader',  # 3/26/12 JJW
            ),
        ),
    ),
]


#TEMPLATE_CONTEXT_PROCESSORS = (
    #"django.contrib.auth.context_processors.auth",
    #"django.core.context_processors.debug",
    #"django.core.context_processors.i18n",
    #"django.core.context_processors.media",
    #"django.core.context_processors.static",
    #"django.core.context_processors.tz",
    #"django.contrib.messages.context_processors.messages",
    #"django.core.context_processors.request",               # JJW 4/2/12
    #"utils.context_processors.settings",                    # JJW 4/2/12
    #"utils.context_processors.models",                      # JJW 4/2/12
    #"quickpages.context_processors.quick_snippets",         # JJW 11/7/15
    #"quickpages.context_processors.quick_snippet_tags",     # JJW 11/7/15
    ##"django_eracks.apps.utils.context_processors.registered",  # JJW 4/22/12
    #"home.context_processors.registration_forms",           # JJW 4/22/12
    #"home.context_processors.cart_variables",               # JJW 6/10/12
    #"home.context_processors.environment",                  # JJW 9/29/13
    #"home.context_processors.google_analytics_tags",        # JJW 11/13/15
    ##'themes.context_processors.themes',                     # JJW 4/16/15
    ##'django_browserid.context_processors.browserid_form',
    ##'django_browserid.context_processors.browserid', # for newer 0.9 bid - removed for 0.11 JJW
#)

#TEMPLATE_DIRS = (
    ## Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    ## Always use forward slashes, even on Windows.
    ## Don't forget to use absolute paths, not relative paths.
    #os.path.join (PROJECT_ROOT, 'templates'),
#)


#here have to specify the path of chromedriver which is installed using npm install chromedriver
CHROME_DRIVER_PATH = '%s/node_modules/chromedriver/lib/chromedriver/chromedriver'%PROJECT_ROOT


# LOCAL SETTINGS - borrowed from Mezzanine

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.

# Instead of doing "from .local_settings import *", we use exec so that
# local_settings has full access to everything defined in this module.
# Also force into sys.modules so it's visible to Django's autoreload.

'''
nfg: django.core.exceptions.ImproperlyConfigured: Unknown parameters: DEBUG

f = os.path.join (PROJECT_ROOT, 'conf', "local_settings_eracks.py")
print f
if os.path.exists(f):
    print 'EXISTS'
    import sys
    import imp
    #module_name = "%s.local_settings" % PROJECT_APP
    module_name = "eracks.local_settings"
    module = imp.new_module (module_name)
    module.__file__ = f
    #sys.modules [module_name] = module
    exec (open (f, "rb").read())
'''

#try:
#    from local_settings import *
#except:
from conf.local_settings_eracks import *  # for wercker, having trouble with relative symlinks


if DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
#else:
#    GZipMidleware...

TEMPLATES [0] ['OPTIONS'] ['debug'] = DEBUG

#try:
#    from themes_settings import *
#except ImportError:
#    pass

#THEMES_USE_TEMPLATE_LOADERS = True
#TEMPLATE_LOADERS += ('themes.loaders.themes.Loader', )
