import os
import asyncio
from anthropic import AsyncAnthropic
from dotenv import load_dotenv  

load_dotenv()

client = AsyncAnthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


async def main() -> None:
    message = await client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude",
            }
        ],
        model="claude-haiku-4-5",
    )
    print(message.content)


asyncio.run(main())