from __future__ import absolute_import, print_function

from .implementation import *  # NOQA
from .manager import ImplementationManager
from .view import *  # NOQA

implementations = ImplementationManager()
register = default_manager.register
unregister = default_manager.unregister
