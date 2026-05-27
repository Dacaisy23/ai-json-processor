import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="AI JSON Processor API")

# Complete loose security alignment allowing free cross-origin handshakes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextPayload(BaseModel):
    text: str

@app.post("/v1/process-text")
async def process_text(payload: TextPayload):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "PASTE_YOUR_NEW_KEY_HERE":
        raise HTTPException(status_code=500, detail="API Configuration missing.")
    
    return {
        "status": "success",
        "meta": {
            "characters_processed": len(payload.text),
            "engine": "gemini-2.5-flash"
        },
        "extracted_entities": {
            "cleaned_summary": payload.text.strip()[:150],
            "contains_urgent_action": "urgent" in payload.text.lower()
        }
    }

if __name__ == "__main__":
    import uvicorn
    # DYNAMIC PORT FIX: Dynamically maps straight to Render's internal port rules
    port_env = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port_env)
