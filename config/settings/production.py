""" 
Settings to import into settings.py for the production environment
"""

from .base import *

# Redis Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": config("REDIS_BACKEND"),
    },
}
