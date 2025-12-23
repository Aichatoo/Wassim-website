"""
⚙️ GUIDE DE CONFIGURATION - settings.py
=======================================

Ce fichier explique les configurations essentielles à ajouter
dans ton fichier settings.py Django pour le site Wassim El Fath.

📌 NE PAS copier-coller tout le fichier settings.py !
   → Ajoute uniquement ces sections à ton settings.py existant

🔒 SÉCURITÉ : Utilise python-decouple pour les secrets
"""

# ==========================================
# 🔐 VARIABLES D'ENVIRONNEMENT (.env)
# ==========================================

"""
Crée un fichier .env à la racine du projet :

# Django
SECRET_KEY=votre-cle-secrete-super-longue-et-complexe-ici
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (formulaire de contact)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=wassimelfath@gmail.com
EMAIL_HOST_PASSWORD=Projet@012026

# Google Analytics
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX

# Base de données (production)
DATABASE_URL=postgres://user:password@host:port/dbname
"""


# ==========================================
# 📦 IMPORTS NÉCESSAIRES
# ==========================================

from decouple import config, Csv
import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# 🔐 SÉCURITÉ
# ==========================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())


# ==========================================
# 📱 APPLICATIONS INSTALLÉES
# ==========================================

INSTALLED_APPS = [
    # 🏠 Ton application
    'home',  # ⚠️ IMPORTANT : Ajouter en premier !
    
    # 🎨 Wagtail CMS
    'wagtail.contrib.forms',       # Formulaires
    'wagtail.contrib.redirects',   # Redirections
    'wagtail.embeds',              # Vidéos YouTube, etc.
    'wagtail.sites',               # Multi-sites
    'wagtail.users',               # Utilisateurs Wagtail
    'wagtail.snippets',            # Snippets réutilisables
    'wagtail.documents',           # Gestion de documents
    'wagtail.images',              # Gestion d'images
    'wagtail.search',              # Recherche
    'wagtail.admin',               # Interface admin
    'wagtail',                     # Core Wagtail
    
    # 🔧 Dependencies Wagtail
    'modelcluster',
    'taggit',
    
    # 🐍 Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


# ==========================================
# 🌐 MIDDLEWARE
# ==========================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Pour les fichiers statiques
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # 🎨 Wagtail middleware
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]


# ==========================================
# 📄 TEMPLATES
# ==========================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # 🎨 Wagtail context processors
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },
]


# ==========================================
# 🗄️ BASE DE DONNÉES
# ==========================================

# 📌 Développement : SQLite (par défaut)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🚀 Production : PostgreSQL (recommandé)
"""
if not DEBUG:
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(
        default=config('DATABASE_URL')
    )
"""


# ==========================================
# 📧 CONFIGURATION EMAIL
# ==========================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# 💡 Note : Pour Gmail, utilise un "mot de passe d'application"
# Guide : https://support.google.com/accounts/answer/185833


# ==========================================
# 🌍 INTERNATIONALISATION
# ==========================================

LANGUAGE_CODE = 'fr-fr'  # 🇫🇷 Français
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True


# ==========================================
# 📁 FICHIERS STATIQUES (CSS, JS, Images)
# ==========================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'home', 'static'),
]

# 🚀 WhiteNoise pour servir les fichiers statiques en production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ==========================================
# 📁 FICHIERS MEDIA (Uploads utilisateur)
# ==========================================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ==========================================
# 🎨 CONFIGURATION WAGTAIL
# ==========================================

WAGTAIL_SITE_NAME = 'Wassim El Fath'

# URL de l'admin Wagtail
WAGTAILADMIN_BASE_URL = 'https://www.wassimelfath.com'  # À changer pour ton domaine

# Désactiver les notifications Wagtail (optionnel)
WAGTAIL_ENABLE_UPDATE_CHECK = False

# Taille maximale des images uploadées
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

# Formats d'images autorisés
WAGTAILIMAGES_EXTENSIONS = ['gif', 'jpg', 'jpeg', 'png', 'webp']


# ==========================================
# 🔐 SÉCURITÉ PRODUCTION
# ==========================================

if not DEBUG:
    # HTTPS
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Autres sécurités
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'


# ==========================================
# 📊 GOOGLE ANALYTICS
# ==========================================

GOOGLE_ANALYTICS_ID = config('GOOGLE_ANALYTICS_ID', default='')


# ==========================================
# 📝 LOGGING (Journaux d'erreurs)
# ==========================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'wagtail': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}


# ==========================================
# 🎯 CONTEXT PROCESSORS PERSONNALISÉS
# ==========================================

"""
Pour rendre les SiteSettings accessibles dans tous les templates,
ajoute ceci à TEMPLATES[0]['OPTIONS']['context_processors'] :

'home.context_processors.site_settings',

Puis crée le fichier home/context_processors.py :
"""

"""
# home/context_processors.py

from home.models import SiteSettings

def site_settings(request):
    '''
    Rend les SiteSettings accessibles dans tous les templates.
    Usage dans les templates : {{ settings.home.SiteSettings.xxx }}
    '''
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
    
    return {
        'site_settings': settings,
    }
"""


# ==========================================
# 🚀 COMMANDES ESSENTIELLES
# ==========================================

"""
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Lancer le serveur de développement
python manage.py runserver

# Lancer le serveur sur toutes les interfaces (pour tester sur mobile)
python manage.py runserver 0.0.0.0:8000
"""


# ==========================================
# 📦 REQUIREMENTS.TXT
# ==========================================

"""
Django>=4.2,<5.0
wagtail>=5.2
Pillow>=10.0.0
python-decouple>=3.8
whitenoise>=6.5.0

# Production (optionnel)
psycopg2-binary>=2.9  # PostgreSQL
gunicorn>=21.2.0      # Serveur WSGI
dj-database-url>=2.1.0
"""


"""
💡 NOTES IMPORTANTES POUR LE DÉVELOPPEUR JUNIOR :

1. 🔐 Variables d'environnement (.env)
   - JAMAIS commiter .env dans Git
   - Ajouter .env dans .gitignore
   - Utiliser python-decouple pour y accéder

2. 📧 Configuration email
   - Gmail nécessite un "mot de passe d'application"
   - Ne PAS utiliser ton mot de passe principal
   - Guide : https://support.google.com/accounts/answer/185833

3. 🗄️ Base de données
   - Développement : SQLite (simple, pas de config)
   - Production : PostgreSQL (robuste, recommandé)

4. 📁 Fichiers statiques
   - STATIC_URL : URL pour accéder aux fichiers (/static/)
   - STATIC_ROOT : Où les fichiers sont collectés (production)
   - STATICFILES_DIRS : Où Django cherche les fichiers (dev)

5. 📁 Fichiers media
   - MEDIA_URL : URL pour accéder aux uploads (/media/)
   - MEDIA_ROOT : Où les fichiers sont stockés

6. 🎨 Wagtail
   - WAGTAIL_SITE_NAME : Nom affiché dans l'admin
   - WAGTAILADMIN_BASE_URL : Ton domaine de production

7. 🔐 Sécurité
   - DEBUG = False en production
   - HTTPS obligatoire en production (SECURE_SSL_REDIRECT)
   - Secret key différente entre dev et prod

8. 📊 Google Analytics
   - Ajouter l'ID dans .env
   - Accessible via config('GOOGLE_ANALYTICS_ID')

9. 🚀 Déploiement
   - Collecter les statiques : collectstatic
   - Utiliser Gunicorn ou uWSGI comme serveur
   - Configurer Nginx ou Apache comme reverse proxy

10. 🐛 Debug
    - Utiliser le fichier debug.log pour les erreurs
    - Activer DEBUG uniquement en développement
"""