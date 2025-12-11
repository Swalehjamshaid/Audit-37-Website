# scheduler.py

import os
import sys
# ... other imports ...

# --- CRITICAL FIX: Add current directory to path for absolute imports ---
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))) 
# -----------------------------------------------------------------------

# --- Absolute Imports ---
from app import app, db, User 
# ... rest of the file ...
