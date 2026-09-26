import httpx2
import os


GITHUB_API_BASE = "https://api.github.com/repos/"
GITHUB_TOKEN = os.environ() 


headers = {
    "Accept": "application/vnd.github+json",
}

# goes from 60/hour to 300hour
if GITHUB_TOKEN:
    headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"


async def 