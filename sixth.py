import os
import logging
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.usage import UsageLimits
from pydantic_ai.exceptions import UsageLimitExceeded
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

# --- Konversationen ---
agent = Agent(model=model, system_prompt="Be a helpful assistant.")
result1 = agent.run_sync("Tell me a joke.")
print(result1.output)
print("-" * 25)
result2 = agent.run_sync("Explain?", message_history=result1.new_messages())
print(result2.output)
print("-" * 25)

# --- Nutzungsbeschränkung ----

agent_n = Agent(model=model)
try:
    result_sync = agent_n.run_sync(
        "What is the capital of Italy? Answer with a paragraph.",
        usage_limits=UsageLimits(response_tokens_limit=10),
    )
except UsageLimitExceeded as e:
    print(e)

print("-" * 25)
agent_param = Agent(model=model)
result_sync = agent_param.run_sync(
    "What is the capital of Italy?",
    model_settings={"temperature": 1.0},
)
print(result_sync.output)
print("-" * 25)
