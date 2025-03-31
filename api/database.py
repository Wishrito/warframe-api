import os
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine

# Database setup - using environment variable for connection string
# For Vercel, you'll need to set up a PostgreSQL database (like Neon, Supabase, etc.)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@localhost:5432/warframe")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
