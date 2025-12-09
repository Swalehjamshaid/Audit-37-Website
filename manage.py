# ───────────────────── TOP OF FILE (add this) ─────────────────────
import os
import sys
from pathlib import Path

# Fix local imports (webaudit folder)
sys.path.insert(0, str(Path(__file__).parent.resolve()))

from fastapi import FastAPI

# Create the app (MUST be named "app" for Railway)
app = FastAPI(title="Audit-37 Website", version="1.0")

# ───────────────────── YOUR EXISTING CODE (keep all your routes) ─────────────────────
# Example – keep or add this test route
@app.get("/")
async def root():
    return {"message": "Audit-37 Website is now LIVE on Railway!"}

# Keep all your existing @app.get(), @app.post(), imports from webaudit, etc.
# Example:
# from webaudit import some_function
# ... your code ...

# ───────────────────── BOTTOM OF FILE (add this) ─────────────────────
# This makes it work both locally and on Railway
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
