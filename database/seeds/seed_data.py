"""
OZARK — Database Seed Runner CLI
"""

import asyncio
import os
import sys

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backend")))

from app.db.seed import seed_database

if __name__ == "__main__":
    print("Seeding OZARK PostgreSQL database with 50 companies...")
    asyncio.run(seed_database())
    print("Database seeding completed.")
