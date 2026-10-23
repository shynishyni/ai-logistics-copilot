import os
import json
import asyncio
from typing import AsyncGenerator, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from google import genai
from google.genai import types

from app.config import settings
from app.api.v1.chat import cruds

SYSTEM_INSTRUCTION = """
You are the AI Logistics Copilot — an expert, high-precision AI assistant specialized in supply chain management, freight shipping, carrier rate calculation, package tracking, and customs compliance.

Your Core Capabilities:
1. Parse natural-language shipment requirements (origin, destination, package dimensions, weight, carrier preference).
2. Calculate accurate rate comparisons across FedEx, UPS, and DHL.
3. Retrieve customs regulations and shipping policies.
4. Track active shipments across checkpoints.
5. Assist with booking execution while respecting safety guardrails.

Style Guidelines:
- Professional, concise, clear, and well-structured markdown outputs.
- Render comparisons using GitHub markdown tables.
- Always provide actionable, clear next steps for logistics workflows.
"""

def get_gemini_client() -> genai.Client:
    api_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        # Fallback or initialization without key (will raise on generation if missing)
        return genai.Client()
    return genai.Client(api_key=api_key)

class ChatService:
    @staticmethod
    async def process_chat(
        db: AsyncSession, 
        session_id: UUID, 
        user_message: str
    ) -> str:
        # 1. Fetch historical context messages from DB
        history = await cruds.get_session_messages(db, session_id)
        
        # 2. Build Gemini contents
        contents = []
        for msg in history:
            if msg.content:
                contents.append(
                    types.Content(
                        role="user" if msg.role == "user" else "model",
                        parts=[types.Part.from_text(text=msg.content)]
                    )
                )

        client = get_gemini_client()
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.3,
        )

        # 3. Call Gemini SDK
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config,
        )

        assistant_text = response.text or "No response generated."
        
        # 4. Save assistant response to DB
        await cruds.add_message(db, session_id, role="assistant", content=assistant_text)
        return assistant_text

    @staticmethod
    async def stream_chat(
        db: AsyncSession, 
        session_id: UUID, 
        user_message: str
    ) -> AsyncGenerator[str, None]:
        # 1. Save user message to database
        await cruds.add_message(db, session_id, role="user", content=user_message)
        
        # 2. Fetch context history
        history = await cruds.get_session_messages(db, session_id)
        
        contents = []
        for msg in history:
            if msg.content:
                contents.append(
                    types.Content(
                        role="user" if msg.role == "user" else "model",
                        parts=[types.Part.from_text(text=msg.content)]
                    )
                )

        client = get_gemini_client()
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.3,
        )

        full_response_text = ""

        try:
            # Generate stream from Gemini SDK
            response_stream = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=contents,
                config=config,
            )

            for chunk in response_stream:
                if chunk.text:
                    full_response_text += chunk.text
                    yield f"data: {json.dumps({'event': 'delta', 'text': chunk.text})}\n\n"
                    await asyncio.sleep(0.01)

            # 3. Save completed assistant message to database
            await cruds.add_message(db, session_id, role="assistant", content=full_response_text)
            yield f"data: {json.dumps({'event': 'done', 'session_id': str(session_id)})}\n\n"

        except Exception as e:
            error_msg = f"Error during generation: {str(e)}"
            yield f"data: {json.dumps({'event': 'error', 'text': error_msg})}\n\n"
