from django.core.exceptions import ImproperlyConfigured
import json


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from unipath import Path
BASE_DIR = Path(__file__).ancestor(3)

with open("secret.json") as f:
    secret = json.loads(f.read())

def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = "la variable %s no existe" % secret_name
        raise ImproperlyConfigured(msg)



SECRET_KEY = get_secret('SECRET_KEY')


# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

LOCAL_APPS = (
    'applications.core',
    
    'applications.users',
    'applications.home',
    'applications.producto',
    'applications.clientes',
    'applications.cuentas',
    #'applications.pedidos',
    'applications.personal',
    'applications.actividades',
    #'applications.movimientos',
    #'applications.movimientosBancarios',
    #'applications.documentos',

    # AREA COMERCIAL
    'applications.COMERCIAL.quotes',
    'applications.COMERCIAL.purchase',
    'applications.COMERCIAL.sales',
    'applications.COMERCIAL.stakeholders',

    'applications.COMERCIAL.reports',

    # AREA FINANCIERA
    'applications.FINANCIERA.movimientosBancarios',
    'applications.FINANCIERA.documentos',

    # AREA LOGISTICA
    'applications.LOGISTICA.transport',

    # AREA PRODUCCION
    'applications.PRODUCTION',

    # AREA RRHH
    'applications.RRHH',

    'multiselectfield',
    'import_export',

    'rest_framework',
)

THIRD_PARTY_APPS = (
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CRM_davinchys.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Context processor personalizado para el menú
                'applications.core.context_processors.menu_navigation',

            ],
        },
    },
]

WSGI_APPLICATION = 'CRM_davinchys.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'es-mx'

PERMISSIONS = {
    'rh': [
        ('add_empleado', 'Puede agregar empleados'),
        ('change_empleado', 'Puede modificar empleados'),
        ('delete_empleado', 'Puede eliminar empleados'),
        ('view_all_asistencia', 'Puede ver toda la asistencia'),
        ('view_all_documentos', 'Puede ver todos los documentos'),
        ('approve_permisos', 'Puede aprobar/rechazar permisos'),
    ]
}

#TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = False
