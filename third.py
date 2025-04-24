import os
import logging
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

from dataclasses import dataclass
import httpx

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv(override=True)
logger.info("Environment variables loading attempt finished.")


llm_api_key = os.getenv("API_KEY", "OLLAMA")
llm_endpoint = os.getenv("BASE_URL", "http://localhost:11434/v1")
llm_model_name = os.getenv("MODEL_NAME", "qwen2.5:latest")
logger.info(f"Using LLM Endpoint: {llm_endpoint}")
logger.info(f"Using LLM Model: {llm_model_name}")

logger.info("Initializing Provider")
provider = OpenAIProvider(base_url=llm_endpoint, api_key=llm_api_key)
logger.info("Provider Initialized")

logger.info("Initializing Model")
model = OpenAIModel(provider=provider, model_name=llm_model_name)
logger.info("Model Initialized")


@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.AsyncClient


agent = Agent(
    model=model,
    deps_type=MyDeps,
)


@agent.system_prompt
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    response = await ctx.deps.http_client.get(
        "https://example.com",
        headers={"Authorization": f"Bearer {ctx.deps.api_key}"},
    )
    response.raise_for_status()
    return f"Prompt: {response.text}"


async def main():
    async with httpx.AsyncClient() as client:
        deps = MyDeps("foo", client)
        result = await agent.run("Tell me a joke.", deps=deps)
        print(result.output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
