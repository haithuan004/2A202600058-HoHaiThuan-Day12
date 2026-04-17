import asyncio

async def generate_response(question: str) -> str:
    """Mock LLM response for local testing without incurring API costs."""
    await asyncio.sleep(1) # Simulate network latency
    return f"I am a mock response to '{question}'"
