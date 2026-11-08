class SimulatedProvider:
    """Respostas fixas, para desenvolver e testar sem chave. A tela deve indicar que é simulado."""

    name = "simulated"

    def generate(self, prompt: str, *, max_tokens: int = 400) -> str:
        return "[simulado] Resposta do agente indisponível sem watsonx.ai configurado."
