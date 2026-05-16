import os
import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent

app = FastAPI(title="AI Chat Agent API")

# Configure CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Simplified for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Runner with auto_create_session=True
session_service = InMemorySessionService()
runner = Runner(
    app_name="AI_Chat_Agent",
    agent=root_agent, 
    session_service=session_service,
    auto_create_session=True
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Get the last message from the user
        user_message_text = request.messages[-1].content
        
        # Wrap in types.Content as expected by ADK Runner
        new_message = types.Content(
            role="user",
            parts=[types.Part(text=user_message_text)]
        )
        
        session_id = "default_session"
        user_id = "default_user"
        
        final_text = ""
        
        # Runner will automatically create the session if it doesn't exist
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message
        ):
            # Collect the final response text
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        final_text += part.text
                    elif isinstance(part, dict) and 'text' in part:
                        final_text += part['text']

        if not final_text:
            final_text = "The agent did not return a response."

        return ChatResponse(response=final_text)
    except Exception as e:
        print(f"Error during agent execution: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
