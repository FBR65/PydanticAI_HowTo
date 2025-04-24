import os
import logging
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

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


class CityLocation(BaseModel):
    city: str
    country: str


agent = Agent(model=model, result_type=CityLocation)
result = agent.run_sync("Wo waren die Olympischen Spiele 2012?")
print(result.output)
