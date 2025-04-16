from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

# Initialize FastAPI app
app = FastAPI()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Pydantic model for request validation
class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 50  # Default max tokens
    temperature: float = 0.7  # Default creativity level

# Pydantic model for response
class ChatResponse(BaseModel):
    response: str

# Endpoint to interact with the chatbot
@app.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    try:
        # Call OpenAI's GPT model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5 Turbo model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )

        # Extract the generated response
        bot_response = response.choices[0].message["content"].strip()
        return ChatResponse(response=bot_response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")