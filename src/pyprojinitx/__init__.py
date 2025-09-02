"""pyprojinitx package entrypoints

Expose a console entrypoint `pyprojinitx` that calls the main function
from the implementation module.
"""

from .__main__ import main

__all__ = ["main"]
