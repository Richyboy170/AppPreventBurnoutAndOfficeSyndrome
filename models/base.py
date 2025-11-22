"""Shared SQLAlchemy base for all models."""
from sqlalchemy.ext.declarative import declarative_base

# Single shared Base for all models to ensure foreign key relationships work
Base = declarative_base()
