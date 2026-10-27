from typing import Protocol


class LLMProvider(Protocol):
    """Interface que todo provedor de modelo cumpre."""

    name: str

    def generate(self, prompt: str, *, max_tokens: int = 400) -> str: ...
