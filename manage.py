#!/usr/bin/env python3
import sys
from pathlib import Path

# CRITICAL: Add current directory to Python path so 'webaudit' is found
sys.path.insert(0, str(Path(__file__).parent.resolve()))

# Now your imports work (keep the rest of your code below)
from fastapi import FastAPI

app = FastAPI(title="Audit-37 Website")  # Make sure this is named 'app'

# Add this test route if not already there (for / endpoint)
@app.get("/")
async def root():
    return {"message": "Audit-37 Website is LIVE! No more errors."}

# Keep ALL your existing code/imports/routes below here
# e.g., from webaudit import whatever  # This now works!
# ... your code ...

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
