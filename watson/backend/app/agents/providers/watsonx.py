from app.config import Settings


class WatsonxProvider:
    """Chama um modelo Granite no watsonx.ai. Precisa do extra `watsonx` instalado."""

    name = "watsonx"

    def __init__(self, settings: Settings) -> None:
        from ibm_watsonx_ai import Credentials
        from ibm_watsonx_ai.foundation_models import ModelInference

        self._model = ModelInference(
            model_id=settings.watsonx_model_id,
            credentials=Credentials(url=settings.watsonx_url, api_key=settings.watsonx_api_key),
            project_id=settings.watsonx_project_id,
        )

    def generate(self, prompt: str, *, max_tokens: int = 400) -> str:
        return self._model.generate_text(prompt=prompt, params={"max_new_tokens": max_tokens})
