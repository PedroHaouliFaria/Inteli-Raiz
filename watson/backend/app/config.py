from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Raiz do repositório: o modelo fica em outputs/ e as bases em data/processed/, como no notebook 03.
REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Configuração lida das variáveis de ambiente (ou do arquivo .env)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./watson.db"
    agent_provider: str = "simulated"
    # Segredo obrigatório para assinar o cookie de sessão (§4 do contrato)
    session_secret: str
    # Cookie Secure só em produção; em dev (False) o cookie funciona em HTTP
    session_secure: bool = False
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    watsonx_api_key: str = ""
    watsonx_project_id: str = ""
    watsonx_model_id: str = "ibm/granite-3-8b-instruct"
    frontend_origin: str = "http://localhost:5173"

    # Política do aviso de compra (decisão 0004). Os dois últimos aguardam a resposta do time.
    notice_medium_threshold: float = 0.60
    notice_high_threshold: float = 0.80
    notice_auto_close_on_it_was_me: bool = True
    notice_response_timeout_minutes: int = 10

    # Tentativas simuladas de rajada (docs/dados/modelo-de-dados.md). Valores iniciais, ajustáveis pelo time.
    burst_velocity_threshold: int = 10
    burst_max_attempts: int = 5
    burst_window_minutes: int = 15
    burst_seed: int = 42

    # Confirmação: prazo em segundos para o associado responder (padrão 15 min)
    confirmation_ttl_seconds: int = 900

    # LLM para o agente de chat (§7 e §10)
    llm_model: str = "groq:openai/gpt-oss-120b"
    groq_api_key: str = ""
    # Limite de mensagens por compra em 10 min (§7)
    chat_rate_limit_messages: int = 20
    chat_rate_limit_window_seconds: int = 600

    # Modelo de risco: "local" lê o .joblib; "watsonx" chama o deployment online no watsonx.ai Runtime.
    risk_model_provider: str = "local"
    risk_model_path: str = str(REPO_ROOT / "outputs" / "modelo_rf.joblib")
    risk_data_dir: str = str(REPO_ROOT / "data" / "processed")
    risk_watsonx_deployment_id: str = ""
    # Limiar F2 do notebook 03: a partir dele o modelo considera a transação fraude.
    risk_decision_threshold: float = 0.817

    # Endpoints de demonstração (§9): só registrados com DEMO_MODE=true
    demo_mode: bool = False


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


def get_burst_simulation_config():
    from app.simulation.burst import BurstSimulationConfig

    s = get_settings()
    return BurstSimulationConfig(
        velocity_threshold=s.burst_velocity_threshold,
        max_attempts=s.burst_max_attempts,
        window_minutes=s.burst_window_minutes,
        seed=s.burst_seed,
    )
