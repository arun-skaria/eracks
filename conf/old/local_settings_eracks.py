# -*- coding: utf-8 -*-
# Django local_settings for eracks10 aka django_eracks project.

import os, socket
import sys
from sh import which

if ( 'APACHE_PID_FILE' in os.environ or  # Apache => production - what about nginx?
     'SERVER_SOFTWARE' in os.environ or  # gunicorn Note: not on current prod or stagin :-( use HNN?
     'UPSTART_JOB' in os.environ         # set up in /etc/init/ on Ubuntu - TODO: this will change in 16.04! use HNN?
   ):
    DEBUG = False
else:
    DEBUG = True
    #print os.environ
    # why do I need this, again? JJW 2/20/14
    #assert '_' in os.environ and os.environ ['_'].endswith (('python', 'manage.py'))

# see https://djangosnippets.org/snippets/2338/ - we should change for non-prod dev sites
GOOGLE_ANALYTICS_ID = 'UA-37665012-1'
GOOGLE_ANALYTICS_DOMAIN = 'eracks.com'

HNN = socket.getfqdn().lower().split('.')
DEV = 'dev' in HNN or not 'eracks' in HNN

#Here assigning emails for staging and other -mani
EMAIL_ID = 'joe@eracks.com'
INFO_EMAIL = 'info@eracks.com'
ORDER_FROM_EMAIL = 'orders@eracks.com'
SECURE_ORDER_EMAIL = ['joe@eracks.com',]
ORDER_EMAIL = ['orders@eracks.com',]
CONTACT_EMAILS = ['info@eracks.com','joe@eracks.com']
HOST_NAME = ''
HOST_URL = ''
TEST_EMAIL = ['joe@eracks.com',]

EMAIL_SUBJECT_PREFIX = 'Error is from %s '%(HNN[0])

FIREFOXPRESENT = False # True if which ('firefox') else False

#CHROMEPRESENT = True if which ('google-chrome') else False
CHROMEPRESENT = True if which ('chromium-browser') else False

USEVIRTUALDISPLAY = True if which ('Xvfb') else False

#SELENIUM_DRIVER = 'Firefox' #give Firefox or give "Chrome" what you want to test with if you run tests in chrome.

# Have to specify the path of chrome driver which is downloaded from http://chromedriver.storage.googleapis.com/index.html
#CHROME_DRIVER_PATH = "/home/nyros/Downloads/chromedriver"
CHROME_DRIVER_PATH = "/usr/lib/chromium-browser/chromedriver"
#CHROME_DRIVER_PATH = "/usr/bin/chromedriver"

#if os.access ('/.d2ockerinit', os.R_OK):
#  CHROME_DRIVER_OPTIONS = '--no-sandbox'

#if 'nyros' in HNN[0]:
#    EMAIL_ID = 'manikantak_nyros@yahoo.com'
#    INFO_EMAIL = 'manikantak_nyros@yahoo.com'
#    ORDER_FROM_EMAIL = 'manikantak_nyros@yahoo.com'
#    SECURE_ORDER_EMAIL = ['manikantak_nyros@yahoo.com']
#    ORDER_EMAIL = ['manikantak_nyros@yahoo.com']
#    CONTACT_EMAILS = ['manikantak_nyros@yahoo.com']
#    HOST_NAME = 'Nyros-eRacks'
#    HOST_URL = 'http://10.90.90.124:8000/'
#    TEST_EMAIL = ['manikantak_nyros@yahoo.com',]
#el
if 'dev' in HNN[0]:
    HOST_NAME = 'Dev-eRacks'
    HOST_URL = 'http://dev.eracks.com/'
elif 'staging' in HNN[0]:
    HOST_NAME = 'Staging-eRacks'
    HOST_URL = 'http://dev.eracks.com/'
elif 'eracks' in HNN[0]:
    #INFO_EMAIL = 'info@eracks.com'
    #ORDER_FROM_EMAIL = 'orders@eracks.com'
    #SECURE_ORDER_EMAIL = ['joe@eracks.com']
    #ORDER_EMAIL = ['orders@eracks.com']
    #CONTACT_EMAILS = ['info@eracks.com','joe@eracks.com']
    HOST_NAME = 'eRacks'
    HOST_URL = 'http://eracks.com/'
    #TEST_EMAIL = ['joe@eracks.com',]
elif 'mintstudio' in HNN[0]:
    HOST_NAME = 'minststudio-eRacks'  # 'http://127.0.0.1'
    TEST_EMAIL = ['joe@eracks.com',]
    EMAIL_EXTRAS_GNUPG_HOME = '/home/joe/.gnupg'
    USEVIRTUALDISPLAY = False

# could also use CI in os.environ, and os.environ ['CI'].lower() == 'true', or WERCKER in os.envo..


print 'DEBUG', DEBUG
print 'HNN', HNN




# True => don't switch to SSL
DEV_SERVER = False  # do we really need a separate setting? this is from Mezzanine, and referenced in SSLRedirectMiddleware

ALLOWED_HOSTS = ['.eracks.com']

if DEBUG or 1:
    ALLOWED_HOSTS += ['216.172.133.15', '216.172.133.16','10.90.90.124','127.0.0.1','localhost']

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Automatically redirect to HTTPS for the URLs specified by SSL_FORCE_URL_PREFIXES
SSL_ENABLED = not DEBUG

# Sequence of URL prefixes that will be forced to run over SSL when SSL_ENABLED is True.
#SSL_FORCE_URL_PREFIXES = ('/admin', '/account')
SSL_FORCE_URL_PREFIXES = ('/', '/admin', '/account', '/checkout')

# True => only URLs specified by the SSL_FORCE_URL_PREFIXES setting will be accessible over SSL, and all other URLs will be redirected back to HTTP if accessed over HTTPS.
SSL_FORCED_PREFIXES_ONLY = True

# Host name that the site should always be accessed via that matches the SSL certificate.
SSL_FORCE_HOST = ''

TESTSERVER = 'testserver' in sys.argv
TESTING = 'test' in sys.argv or 'testserver' in sys.argv
LOADING_FIXTURES = 'loaddata' in sys.argv
NODB_COMMAND = 'compilethemes'  in sys.argv or \
    'collectstatic' in sys.argv or \
    'fb_version_generate' in sys.argv

if 'test' in sys.argv:
    DATABASES = dict (
        default = dict (
            ENGINE = 'django.db.backends.sqlite3',
            TEST = dict (
                #NAME = 'testeracksdb',              # setting NAME here means don't create in-memory sqlite test db
                SERIALIZE = False
            )
        ),
    )
    if TESTSERVER:
        DATABASES ['default'] ['TEST'] ['NAME'] = 'testeracksdb'
else:
    DATABASES = dict (
        default = dict (
            ENGINE = 'django.db.backends.postgresql_psycopg2',        #, 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            NAME = 'eracksdb',              # Or path to database file if using sqlite3.
            USER = 'eracks',                # Not used with sqlite3.
            PASSWORD = 'Wav3lets9',         # Not used with sqlite3.        # Not used with sqlite3.
            # HOST = 'eracks.com',          # Set to empty string for localhost. Not used with sqlite3.
            # PORT = '5432',                # Set to empty string for default. Not used with sqlite3.
            HOST = '127.0.0.1',             # Set to empty string for localhost. Not used with sqlite3.
            PORT = '5432',                  # Set to empty string for default. Not used with sqlite3.
            AUTOCOMMIT = True,
            # OPTIONS = dict (
            #     autocommit=True,
            # )
        )
    )


ROOT_URLCONF = 'eracks.urls'


# new TEMPLATES dict for 1.8 - moved to main settings.py


THEMES = ('tshop', 'assan', 'unify', 'legacy')
DEFAULT_THEME = 'tshop'
#DEFAULT_THEME = 'legacy'  # uncomment for testing - JJW

# not a good idea, this wants *all* the migrations for auth
#MIGRATION_MODULES = { 'auth': 'customer.migrations.auth' }


INSTALLED_APPS = (

    # Monkey patch for lengthen username for long emails -
    # on a new db: uncomment, make & run migrations, then comment again :)
    # migrations will be created in, and run from, the Django tree.
    #'monkey_patch',

    #### Admin & related admin apps which need to be before Django Admin apps
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',  # must be before admin

    #### Django admin & related apps which should be before other project apps
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.auth',
    # 'django.contrib.formtools',  # for preview
    #'django_browserid',  # Load after auth to monkey-patch it.
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',  # yuk
    'django.contrib.redirects',
    'django.contrib.sitemaps',
    'haystack',  # docs say it needs to be above your apps - see http://django-haystack.readthedocs.org/en/v1.2.7/tutorial.html
    #'userena',  # needs to be before customers to unregister-reregister admin
    'memcache_status',
    #'themes',  # themes need to be at the top so templates are found here 1st
    'stheme',

    #### internal apps:
    'home',
    'customers',
    'orders',
    #'legacy',
    'products',
    'bloglets',
    'utils',
    'catax',
    'sqls',
    'quotes',

    #### projects dir
    #'django_stylus', # jjw
    #'djgrid',
    #'obdjects', # deprecated - snippets moved to quickpages.QuickSnippets 11/7/15 jjw
    'quickpages', # jjw

    #### 3rd party:
    'loginas',
    #'pyjade',
    'django_countries',  # countries list and field https://bitbucket.org/smileychris/django-countries
    'codemirror2',
    'debug_toolbar',
    'djide',
    #'dbtemplates',  # retired 6/10/12 JJW
    #'aloha',  # out temporarily, migrate to alternate https://github.com/ntucker/django-aloha-edit - JJW
    'coffeescript',
    'django_wysiwyg', # try without it 9/6/16 JJW - nope, quickpages uses it
    #'django_bfm',
    'userena',
    'guardian', # required by userena
    #'apps',  # reposition Admin for snippets into quickpages
    #'filer',
    'easy_thumbnails',  # reqd by filer, userena
    'taggit',
    #'taggit_templatetags',
    # 'social_auth',     #Removing django-social-auth and using python-social-auth
    'social.apps.django_app.default', #this is for python-social-auth
    #'socialregistration',
    #'socialregistration.contrib.linkedin',
    'email_extras',
    #'csvimport',  # JJW 4/24/14 - commented out 10/11/14 for django 1.7 until ready
    'csvimport.app.CSVImportConf',   # JJW 1/30/15 now testing 2.4 w/dj1.7
    'django_extensions',
    'webshell',
    'easy_select2',
    #'compressor',

    #### Shop:
    #'plata',
    #'plata.contact', # Not strictly required (contact model can be exchanged)
    #'plata.discount',
    #'plata.payment',
    #'plata.shop',
    'lastmodule',
)


#### for DB Templates
#DBTEMPLATES_USE_CODEMIRROR = True
#DBTEMPLATES_MEDIA_PREFIX = '/static/dbtemplates/'


#### For Django Debug Toolbar
INTERNAL_IPS = (
    #'127.0.0.1',
    #'216.103.147.100',     # torrance hospital 6/15/12 :)  7/17/12 :-(
    #'96.249.201.237',      # sheldon 6/16/12
    #'173.67.120.167',      # sheldon 1/3/12
    #'68.65.169.163',       # stanford 7/26/12
    #'68.65.169.138',       # stanford 7/26/12 - why is this different?
    #'96.238.223.233',      # Sheldon 9/29/13
    #'108.42.142.154',      # Sheldon 10/21/14

    #'108.42.123.186',      # Sheldon 9/27/15
    '108.42.121.168',       # Sheldon 9/6/16
    '68.4.180.198',         # Mom's, San Pedro 10/6/13
    )

#def custom_show_toolbar(request):
#    print 'AHA', request.get_host(), request.META ['REMOTE_ADDR']
#    return True # Always show toolbar, for example purposes only.

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    #'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    #'EXTRA_SIGNALS': ['myproject.signals.MySignal'],
    #'HIDE_DJANGO_SQL': False,  # default: True
    #'TAG': 'div',  # default: body
    #'ENABLE_STACKTRACES' : True,
}

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    #'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
#DEBUG_TOOLBAR_PANELS += ('w3c_validator.panels.W3CValidatorPanel',)


#### For django-wysiwyg

DJANGO_WYSIWYG_FLAVOR = 'ckeditor'
# The following editors are supported out of the box:
#
#    yui - The YAHOO editor.
#    yui_advanced - The YAHOO editor with more toolbar buttons.
#    ckeditor - The CKEditor, formerly known as FCKEditor
#
# It's also possible to add new editors, see extending django-wysiwyg

# JJW 9/27/15 Use CDN:
#DJANGO_WYSIWYG_MEDIA_URL = '//cdn.ckeditor.com/4.5.3/standard/' # already appended in includes.html: 'ckeditor.js'
DJANGO_WYSIWYG_MEDIA_URL = '//cdn.ckeditor.com/4.5.3/full-all/' # basic standard, standard-all, full, full-all


#### for django-filebrowser
FILEBROWSER_DIRECTORY = ''


#### For JJW's expermental developer autorelaod - True => enable my js AUTORELOAD functionality, in base template
AUTORELOAD = False  # DEBUG


#### True => load the Aloha css/js in the base template - you still have to load the aloha tags in your template though
ALOHA = False  # DEBUG


#### For django.contrib.auth UserProfile & Userena
#AUTH_PROFILE_MODULE = 'customers.UserenaProfile'
AUTH_PROFILE_MODULE = 'customers.Customer'

#### Userena, guardian, BrowserID, social_auth
USERENA_DEFAULT_PRIVACY = 'closed'  # 'registered' allows registered users to see each other, 'open' allows all to see all
USERENA_ACTIVATION_REQUIRED = False
AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.yahoo.YahooOpenId',
    'social.backends.github.GithubOAuth2',
    'social.backends.linkedin.LinkedinOAuth',
    'social.backends.dropbox.DropboxOAuth',
    'social.backends.persona.PersonaAuth',
    'django.contrib.auth.backends.ModelBackend',  # move to end if using social_auth
    #'django_browserid.auth.BrowserIDBackend',       # for django-browserid
    # Userena:
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    # #socialregistration:
    # #'socialregistration.contrib.linkedin.auth.LinkedInAuth',
    # # social_auth:
    # 'social_auth.backends.contrib.linkedin.LinkedinBackend',  # no email!
    # 'social_auth.backends.twitter.TwitterBackend',
    # 'social_auth.backends.facebook.FacebookBackend',
    # #'social_auth.backends.google.GoogleOAuthBackend',
    # #'social_auth.backends.google.GoogleOAuth2Backend',
    # 'social_auth.backends.google.GoogleBackend',
    # #'social_auth.backends.yahoo.YahooBackend',
    # 'social_auth.backends.contrib.github.GithubBackend',
    # 'social_auth.backends.contrib.dropbox.DropboxBackend',
    # #'django.contrib.auth.backends.ModelBackend',
)

#if 0 and DEBUG:
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'mail.eracks.com'
    EMAIL_PORT = 25  # 567  # 25  # 2525 # 465 # 25
    # JJW 8/6/16
    EMAIL_HOST_USER = 'relay@librehost.com'
    EMAIL_HOST_PASSWORD = 'allow!'
    EMAIL_USE_TLS = True

    #if 'mintstudio' in HNN[0]:
    #  EMAIL_HOST = 'smtp.verizon.net'
      #EMAIL_HOST_USER = 'relay@librehost.com'
      #EMAIL_HOST_PASSWORD = 'allow'
    #  EMAIL_USE_TLS = True
    #  EMAIL_PORT = 465  # 567  # 25  # 2525 # 465 # 25

# for django-guardian
ANONYMOUS_USER_ID = -1

# for social_auth:
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True
#Old:
#LINKEDIN_CONSUMER_KEY          = '20qhsfqxi4t3'
#LINKEDIN_CONSUMER_SECRET       = 'pYLru1MTqxAnQvmi'
# commented below lines to replace with python-social-auth keys
# LINKEDIN_CONSUMER_KEY           = 'zy6tydz4ot9r'
# LINKEDIN_CONSUMER_SECRET        = 'NkNycVC9phkoG8ST'
#for Python-Social-Auth
SOCIAL_AUTH_LINKEDIN_KEY = 'zy6tydz4ot9r'  #'750fxutaxyqa77'
SOCIAL_AUTH_LINKEDIN_SECRET = 'NkNycVC9phkoG8ST'   #'yGtKq5joLmmwGnTz'
# Add email to requested authorizations.
SOCIAL_AUTH_LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress']
# Add the fields so they will be requested from linkedin.
SOCIAL_AUTH_LINKEDIN_FIELD_SELECTORS = ['email-address', 'headline', 'industry']
# Arrange to add the fields to UserSocialAuth.extra_data
SOCIAL_AUTH_LINKEDIN_EXTRA_DATA = [('id', 'id'),
                                   ('firstName', 'first_name'),
                                   ('lastName', 'last_name'),
                                   ('emailAddress', 'email_address'),
                                   ('headline', 'headline'),
                                   ('industry', 'industry')]


# LINKEDIN_EXTRA_DATA             = [('main-address','main-address'),('phone-numbers','phone-numbers'),('bound-account-types','bound-account-types')]  # [('email', 'email')]
# LINKEDIN_EXTRA_FIELD_SELECTORS  = ['main-address','phone-numbers','bound-account-types']  # ['email']
# commented below lines to replace with python-social-auth keys
# FACEBOOK_APP_ID                 = '151775531612916'
# FACEBOOK_API_SECRET             = 'b3e8d3c5d8ca159a63b06eb5a1bbf691'
#for Python-Social-Auth
SOCIAL_AUTH_FACEBOOK_KEY = '151775531612916'  #'1511891465732329'
SOCIAL_AUTH_FACEBOOK_SECRET = 'b3e8d3c5d8ca159a63b06eb5a1bbf691'  #'6282798c9e8194f1bf55c5c1dda77f7f'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_photos']

# FACEBOOK_EXTENDED_PERMISSIONS   = ['email']
# FACEBOOK_EXTRA_DATA             = [('email', 'email')]
# commented below lines to replace with python-social-auth keys
# TWITTER_CONSUMER_KEY            =  'O7uvpmrWFm6ks54D7Kow'
# TWITTER_CONSUMER_SECRET         = 'Bjh8KTrtYNdiDmdF1s2TwMYXK8sdk0isLHxf4rRbrY'
#for Python-Social-Auth
SOCIAL_AUTH_TWITTER_KEY = 'O7uvpmrWFm6ks54D7Kow'   #'1sw48hsWdtQyvOb5b1pXUuPSr'
SOCIAL_AUTH_TWITTER_SECRET = 'Bjh8KTrtYNdiDmdF1s2TwMYXK8sdk0isLHxf4rRbrY'  #'uoabUpHPgT6eYSkgFw601zc1qmwP9IXV5CM9dv1jJD0IbFz2vT'
# SOCIAL_AUTH_TWITTER_SCOPE = ['email', 'user_photos']

# TWITTER_EXTENDED_PERMISSIONS    = ['email']
# TWITTER_EXTRA_DATA              = [('email', 'email')]
# commented below lines to replace with python-social-auth keys
# GITHUB_APP_ID                   = '9e21e195c19e04c51e75'
# GITHUB_API_SECRET               = '50b02ed8b3b0aaecd4b0801259eea5793cb77e17'
#for Python-Social-Auth
SOCIAL_AUTH_GITHUB_KEY = '9e21e195c19e04c51e75'  #'8b884f2227fd04df1115'
SOCIAL_AUTH_GITHUB_SECRET = '50b02ed8b3b0aaecd4b0801259eea5793cb77e17'  #'3ae408a85c7aea1b7c129e2901b2e2f266b2605c'
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

# GITHUB_EXTENDED_PERMISSIONS     = ['email']
# GITHUB_EXTRA_DATA               = [('email', 'email')]
# commented below lines to replace with python-social-auth keys
# DROPBOX_APP_ID                  = 'feokr5j5kctsmvw'
# DROPBOX_API_SECRET              = '4lzeucdbluzqxs2'
#for Python-Social-Auth
SOCIAL_AUTH_DROPBOX_KEY = 'feokr5j5kctsmvw'
SOCIAL_AUTH_DROPBOX_SECRET = '4lzeucdbluzqxs2'
#GOOGLE_SREG_EXTRA_DATA          = [('email', 'email')]
#GOOGLE_AX_EXTRA_DATA            = [('email', 'email')]
# commented below lines to replace with python-social-auth keys
# GOOGLE_OAUTH2_CLIENT_ID         = '137682524779.apps.googleusercontent.com'
# GOOGLE_OAUTH2_CLIENT_SECRET     = 'g0rihndQFstz7oHIDUieBYub'
#for Python-Social-Auth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '137682524779.apps.googleusercontent.com'   #'642607826843-ggqlpgs8gjo59ehl1vkbca96c2crofrq.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'g0rihndQFstz7oHIDUieBYub'   #'AW-ri41Nu_0bn0ptxaLMGE6l'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']
#GOOGLE_OAUTH_EXTRA_SCOPE        = ['email']

# for socialregistration:
#LINKEDIN_CONSUMER_KEY        = 'zy6tydz4ot9r'
#LINKEDIN_CONSUMER_SECRET_KEY = 'NkNycVC9phkoG8ST'


#### for django-browserID - also inserted auth-backend, see above in the Userena settings, and context processor
SITE_URL = ('http://127.0.0.1:8000',
            'http://www.eracks.com', 'http://dev.eracks.com', 'http://eracks.com',
            'https://www.eracks.com', 'https://dev.eracks.com', 'https://eracks.com',
            'http://216.172.133.15', 'http://216.172.133.15:8000',
            'http://216.172.133.16', 'http://216.172.133.16:8000', )

# new for 0.10, 0.11?
# Added the dev url to access Mozila persona/browser-id
# Added production url to access Mozila persona/browser-id
BROWSERID_AUDIENCES = ['https://dev.eracks.com','http://dev.eracks.com:8000/', '216.172.133.16', 'http://216.172.133.16:8000/','http://10.90.90.124:8000/','http://dev.eracks.com/','http://eracks.com/','https://eracks.com/']

BROWSERID_CREATE_USER = True

def username(email):
    trace = 0

    if trace: print 'In BrowserID callback:', email
    #return email # nope - can't use raw email, because userena can't deal with the @ on the reverse url
    from django.contrib.auth.models import User
    uname = email.split('@', 1)[0]
    existing = User.objects.filter (username__istartswith=uname).values_list ('username', flat=True)
    add_integer = 1

    # still a timing hole here...
    while uname in existing:
        uname = '%s%s' % (email.rsplit('@', 1)[0], add_integer)
        add_integer += 1

    return uname
    #nope: won't fit into 30 chars: joseph_dot_wolff_at_gmail_dot_com
    #return email.replace ('@', '_at_').replace ('www.','').replace('.','_dot_')
    # could use dot-com as the default, & remove:
    #return email.replace ('@', '_at_').replace ('www.','').replace ('.com','').replace('.','_dot_')  # .rsplit('@', 1)[0]
    # could also add a number, incrementally count up to an available one, or use a db seq/id

BROWSERID_USERNAME_ALGO = username

# Path to redirect to on successful login.
LOGIN_REDIRECT_URL = '/'

# Path to redirect to on unsuccessful login attempt.
LOGIN_REDIRECT_URL_FAILURE = '/'

# Path to redirect to on logout.
LOGOUT_REDIRECT_URL = '/'

if DEBUG:
  LOGGING = {
    'version': 1,
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django_browserid': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
  }

#BROWSERID_SHIM = ''
#BROWSERID_VERIFY_CLASS = 'utils.MyVerifyClass' see note in utils - no longer need workaround for autologin


#### Haystack settings

# 1.2.x settings:
#HAYSTACK_SITECONF = 'django_eracks.conf.haystack'
#HAYSTACK_SEARCH_ENGINE = 'simple'
# 2.0.0 beta settings:
#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
#    },
#}
import os
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join (os.path.dirname (os.path.dirname (__file__)), 'eracks', 'whoosh_index'),
    },
}


#### for testing 7/26/12 JJW
#DISABLE_TRANSACTION_MANAGEMENT  = True


#### django-email_extras - gnupg-encrypted emails
# Boolean that controls whether the PGP encryption features are used. Defaults to True if EMAIL_EXTRAS_GNUPG_HOME is specified
#EMAIL_EXTRAS_USE_GNUPG
# String representing a custom location for the GNUPG keyring.
if not 'EMAIL_EXTRAS_GNUPG_HOME' in locals():
  EMAIL_EXTRAS_GNUPG_HOME = '/home/sysadmin/.gnupg'
#EMAIL_EXTRAS_GNUPG_HOME = '/var/gnupg'
# Skip key validation and assume that used keys are always fully trusted.
EMAIL_EXTRAS_ALWAYS_TRUST_KEYS = True


#### Add Memcache 1/23/13 JJW

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


#html validator settings
HTMLVALIDATOR_ENABLED = True

#HTMLVALIDATOR_DUMPDIR = './validationerrors/' # default it /tmp

HTMLVALIDATOR_OUTPUT = 'stdout'

#### starts with memcache, writes thru to DB  9/24/13 JJW

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

# new for 1.7 - JJW
#SESSION_SERIALIZER = "django.core.serializers.json.DjangoJSONEncoder"
#SESSION_SERIALIZER = "django.core.serializers.pyyaml"
SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"


#### django_csvimport
CSVIMPORT_LOG = 'logger'


#### For Django-compressor - see also staticfiles-finders
#COMPRESS_ENABLED = True
