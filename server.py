import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from fastapi.responses import FileResponse  # This is new
import uvicorn
import aiofiles
# --- 1. PASTE YOUR *NEW* API KEY HERE ---

# --- 2. YOUR WORKFLOW ID ---
WORKFLOW_ID = "wf_69055a14b5d481908dc7b441696562b008626578dc8f23d2"


# --- (No need to edit below this line) ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI()

# ENDPOINT 1: The API for ChatKit
@app.post("/api/chatkit/session")
def create_chatkit_session():
    print("Request received: /api/chatkit/session")
    try:
        session = client.beta.chatkit.sessions.create(
            workflow={"id": WORKFLOW_ID},
            user="local-test-user"
        )
        print("Session created successfully.")
        return {"client_secret": session.client_secret}
    
    except Exception as e:
        print(f"Error creating session: {e}")
        return {"error": str(e)}

# ENDPOINT 2: This serves your index.html file
@app.get("/")
async def get_index():
    print("Request received: / (serving index.html)")
    return FileResponse('index.html')


if __name__ == "__main__":
    # --- THIS PRINT STATEMENT IS NOW CORRECT ---
    print(f"Starting ONE server on http://localhost:8000")
    print(f"Using Workflow ID: {WORKFLOW_ID}")
    
    # --- THIS WARNING IS NOW CORRECT ---
    
    # --- THIS PORT IS CORRECT ---
    uvicorn.run(app, host="127.0.0.1", port=8000)