import os
import logging
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv
import asyncio

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

agent = Agent(model=model)

# --- Synchronous Run ---


def sync():
    result_sync = agent.run_sync("Wie heisst die Hauptstadt von Italien??")
    print(result_sync.output)


# --- Asynchronous Calls ---
async def main():
    result = await agent.run("Wie heisst die Hauptstadt von Deutschland?")
    print(result.output)

    async with agent.run_stream("Wie heisst die Hauptstadt von Norwegen?") as response:
        print(await response.get_output())


if __name__ == "__main__":
    asyncio.run(main())
    sync()
