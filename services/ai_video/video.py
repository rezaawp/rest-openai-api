
import asyncio

from openai import AsyncOpenAI
import os

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def generate_video_prompt(prompt, seconds = "4", model="sora-2"):
    return await client.videos.create(
        model=model,
        prompt=prompt,
        seconds=seconds
    )

async def download_video_content(id: str) -> None:
    content = await client.videos.download_content(id, variant="video")
    content.write_to_file(f"static/{id}.mp4")

    return True