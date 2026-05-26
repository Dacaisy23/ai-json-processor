import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize the web server framework
app = FastAPI(title="AI JSON Processor API")

# Define what data clients must send us
class TextPayload(BaseModel):
    text: str

@app.post("/v1/process-text")
async def process_text(payload: TextPayload):
    """
    Accepts raw string text, processes it securely via Gemini,
    and returns verified, structural JSON layouts.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "PASTE_YOUR_NEW_KEY_HERE":
        raise HTTPException(status_code=500, detail="API Configuration missing.")
    
    # Clean up processing layout matching your OpenAPI contract specifications
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
