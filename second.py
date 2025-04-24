import os
import logging
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv
import random

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


agent = Agent(
    model=model,
    deps_type=str,
    system_prompt=(
        """Du bist ein Würfelspielspieler. Werf den Würfel und schau, ob die Zahl, die du erhältst, mit der Vermutung des Nutzers übereinstimmt. 
        Wenn ja, teile ihm mit, dass er gewonnen hat. Nenne den Namen des Spielers in der Antwort."""
    ),
)


@agent.tool_plain
def roll_die() -> str:
    """Roll a six-sided die and return the result."""
    return str(random.randint(1, 6))


@agent.tool
def get_player_name(ctx: RunContext[str]) -> str:
    """Get the player's name."""
    return ctx.deps


if __name__ == "__main__":
    name = "Frank"
    guess = "2"
    dice_result = agent.run_sync(f"Meine Vermutung: {guess}", deps=name)
    print(dice_result.output)
