import environ
root = environ.Path(__file__) - 2  # three folder back (/a/b/c/ - 3 = /)
root_path = root.path()
env = environ.Env(DEBUG=(bool, False),)  # set default values and casting
environ.Env.read_env('settings.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'bootstrapform',
    'taggit',
    'imagekit',
    'django_summernote',
    'datetimewidget',

    'blog.apps.BlogConfig',
    'whitenoise.runserver_nostatic',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [root_path('templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    #'default': env.db(),
     'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'OPTIONS': {
             'options': '-c search_path=public'
         },
         'NAME': 'blog',
         'USER': 'webadmin',
         'PASSWORD': 'FPSvmg03241',
         'HOST': '10.100.3.105',
         'PORT': '5432',
         'CONN_MAX_AGE': None,
     },
}

DATABASES['default']['OPTIONS'] = {
    'options': '-c search_path=public'
}
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', None)

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'blog.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = '/accounts/profile/'
LOGIN_URL = '/accounts/login/'

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
# ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGOUT_ON_GET = True

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = root_path('static_root')

STATICFILES_DIRS = (
    root_path('static'),
)

# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

MEDIA_ROOT = root_path('media')

MEDIA_URL = '/media/'

SESSION_COOKIE_NAME = 'sess_pk'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TAGGIT_CASE_INSENSITIVE = True
# TAGGIT_TAGS_FROM_STRING = 'appname.utils.comma_splitter'
# TAGGIT_STRING_FROM_TAGS = 'appname.utils.comma_joiner'

from django_summernote.settings import static_url

SUMMERNOTE_CONFIG = {
    'iframe': False,
    'airMode': False,
    'styleWithTags': True,
    'direction': 'ltr',
    'width': '100%',
    'height': '480',
    'lang': None,
    'toolbar': [
        ['style', ['style']],
        ['style', ['bold', 'italic', 'underline', 'clear']],
        ['para', ['ul', 'ol', 'height']],
        ['insert', ['link']],
    ],
    'attachment_require_authentication': True,
    'external_css': (
        '//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css',
    ),
    'external_js': (
        '//code.jquery.com/jquery-1.9.1.min.js',
        '//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js',
    ),
    'internal_css': (
        static_url('django_summernote/summernote.css'),
    ),
    'internal_js': (
        static_url('django_summernote/jquery.ui.widget.js'),
        static_url('django_summernote/jquery.iframe-transport.js'),
        static_url('django_summernote/jquery.fileupload.js'),
        static_url('django_summernote/summernote.min.js'),
    ),
    'codemirror': {
            'theme': 'monokai',
    },

}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
