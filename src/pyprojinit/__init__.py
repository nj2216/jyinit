"""pyprojinit package entrypoints

Expose a console entrypoint `pyprojinit` that calls the main function
from the implementation module.
"""

from .pyprojinit import main

__all__ = ["main"]
