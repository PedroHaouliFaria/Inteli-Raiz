"""Provedores de modelo de linguagem. O resto do código só conhece a interface LLMProvider."""

from functools import lru_cache

from app.agents.providers.base import LLMProvider
from app.config import get_settings


@lru_cache
def get_agent_provider() -> LLMProvider:
    settings = get_settings()
    if settings.agent_provider == "watsonx":
        from app.agents.providers.watsonx import WatsonxProvider

        return WatsonxProvider(settings)
    from app.agents.providers.simulated import SimulatedProvider

    return SimulatedProvider()
