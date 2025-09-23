"""
Persona Generator - A powerful tool for generating detailed personas using AI models.

This package provides a flexible, schema-based approach to persona generation
with support for multiple AI models and customizable output formats.
"""

from .exporters.persona_exporter import PersonaExporter
from .factories.persona_factory import PersonaFactory
from .generators.openai import OpenAIGenerator
from .models.characteristics import Characteristic
from .models.persona import Persona
from .models.schema import Schema

__version__ = "1.0.0"
__author__ = "Ciro Gamboa"
__email__ = "ciro@example.com"

__all__ = [
    "PersonaFactory",
    "OpenAIGenerator",
    "PersonaExporter",
    "Persona",
    "Characteristic",
    "Schema",
]
