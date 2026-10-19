"""
EV Share Configuration Package
"""
from .database import connect_db

# Automatically initialize database connection when Django starts
connect_db()
