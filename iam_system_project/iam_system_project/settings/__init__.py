from .base import *

# Import environment-specific settings
try:
    from .development import *
except ImportError:
    pass

try:
    from .database import *
except ImportError:
    pass