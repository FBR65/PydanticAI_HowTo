### ACHTUNG NICHT LAUFFÄHIG ###


# --- Tool Registrierung ---
from pydantic_ai import Agent, RunContext

agent_a = Agent(
    model=model,
    deps_type=str,
    tools=[lambda: str(random.randint(1, 6)), lambda ctx: ctx.deps],
)


# ---- Tool Schema ---

from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelResponse
from pydantic_ai.models.function import AgentInfo, FunctionModel

agent = Agent()


@agent.tool_plain
def foobar(a: int, b: str, c: dict[str, list[float]]) -> str:
    """Get me foobar.
    Args:
        a: apple pie
        b: banana cake
        c: carrot smoothie
    """
    return f"{a} {b} {c}"


# ---- Dynamic Tools ---

from typing import Union
from pydantic_ai import Agent, RunContext
from pydantic_ai.tools import ToolDefinition


agent = Agent("test")


async def only_if_42(
    ctx: RunContext[int], tool_def: ToolDefinition
) -> Union[ToolDefinition, None]:
    if ctx.deps == 42:
        return tool_def


@agent.tool(prepare=only_if_42)
def hitchhiker(ctx: RunContext[int], answer: str) -> str:
    return f"{ctx.deps} {answer}"


result = agent.run_sync("testing...", deps=41)
print(result.data)
# > success (no tool calls)

result = agent.run_sync("testing...", deps=42)
print(result.data)
# > {"hitchhiker":"42 a"}
