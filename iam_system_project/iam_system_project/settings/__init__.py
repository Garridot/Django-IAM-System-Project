from .base import *

# Import environment-specific settingss

try:
    from .email import *
except ImportError:
    pass

try:
    from .development import *
except ImportError:
    pass

try:
    from .database import *
except ImportError:
    pass

try:
    from .celery_settings import *
except ImportError:
    pass
