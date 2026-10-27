from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuração lida das variáveis de ambiente (ou do arquivo .env)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./watson.db"
    agent_provider: str = "simulated"
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    watsonx_api_key: str = ""
    watsonx_project_id: str = ""
    watsonx_model_id: str = "ibm/granite-3-8b-instruct"
    frontend_origin: str = "http://localhost:5173"

    # Política do aviso de compra (decisão 0004). Os dois últimos aguardam a resposta do time.
    notice_medium_threshold: float = 0.60
    notice_high_threshold: float = 0.80
    notice_auto_close_on_it_was_me: bool = True
    notice_response_timeout_minutes: int = 30


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_notice_policy():
    from app.domain.notices.policy import NoticePolicy

    s = get_settings()
    return NoticePolicy(
        medium_threshold=s.notice_medium_threshold,
        high_threshold=s.notice_high_threshold,
        auto_close_on_it_was_me=s.notice_auto_close_on_it_was_me,
        response_timeout_minutes=s.notice_response_timeout_minutes,
    )
