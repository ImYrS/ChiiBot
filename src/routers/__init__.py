"""Routers packages."""

from .admin import router as admin
from .basic import router as basic
from .forward import router as forward
from .setup import router as setup
from .topic import router as topic

# "forward" must be the last one to be imported
__all__ = ["basic", "admin", "topic", "setup", "forward"]
