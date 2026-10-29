"""Testa que o _SYSTEM_PROMPT contém as regras comportamentais exigidas
e que o padrão de llm_model está atualizado."""
from __future__ import annotations

import importlib


def test_llm_model_default():
    """O padrão de llm_model deve ser groq:openai/gpt-oss-120b."""
    import app.config as cfg_module
    # Garante leitura sem cache de variável de ambiente anterior
    cfg_module.get_settings.cache_clear()
    import os
    env_backup = os.environ.pop("LLM_MODEL", None)
    try:
        cfg_module.get_settings.cache_clear()
        settings = cfg_module.Settings(session_secret="test-secret")
        assert settings.llm_model == "groq:openai/gpt-oss-120b", (
            f"llm_model padrão errado: {settings.llm_model}"
        )
    finally:
        if env_backup is not None:
            os.environ["LLM_MODEL"] = env_backup
        cfg_module.get_settings.cache_clear()


def _get_prompt() -> str:
    import app.domain.agent as agent_module
    return agent_module._SYSTEM_PROMPT


def test_prompt_single_purchase_scope():
    """Regra 9: conversa restrita à compra desta tela; outro código proibido."""
    prompt = _get_prompt()
    assert "única compra" in prompt or "esta tela" in prompt, (
        "Prompt deve restringir a conversa à compra desta tela"
    )
    assert "T-011" in prompt or "outro código" in prompt.lower() or "outro código" in prompt, (
        "Prompt deve mencionar que outro código não é permitido"
    )


def test_prompt_no_score_disclosure():
    """Regra 10: nunca informar o score ao associado."""
    prompt = _get_prompt()
    assert "score" in prompt.lower(), "Prompt deve mencionar score"
    # Garante que a proibição de divulgar está presente
    assert (
        "nunca informe o valor do score" in prompt.lower()
        or "não informe o valor do score" in prompt.lower()
        or "nunca informe" in prompt.lower()
    ), "Prompt deve proibir divulgar o score ao associado"


def test_prompt_call_tool_before_answering():
    """Regra 11: chamar consultar_compra antes de responder sobre a compra."""
    prompt = _get_prompt()
    assert "consultar_compra" in prompt, (
        "Prompt deve exigir chamada de consultar_compra antes de responder sobre a compra"
    )
    assert "consultar_status" in prompt, (
        "Prompt deve exigir chamada de consultar_status para prazo/situação"
    )


def test_prompt_no_internal_codes_in_response():
    """Regra 12: usar rótulos, não códigos internos como CARTAO_NAO_PRESENTE."""
    prompt = _get_prompt()
    assert "CARTAO_NAO_PRESENTE" in prompt, (
        "Prompt deve citar CARTAO_NAO_PRESENTE como exemplo proibido"
    )
    assert "rótulo" in prompt.lower() or "rótulos" in prompt.lower(), (
        "Prompt deve instruir a usar rótulos em vez de códigos"
    )


def test_prompt_no_invented_buttons():
    """Regra 13: não inventar botões ou passos; usar solicitar_revisao."""
    prompt = _get_prompt()
    assert "solicitar_revisao" in prompt, (
        "Prompt deve referenciar solicitar_revisao para revisão humana"
    )
    assert (
        "não invente botões" in prompt.lower()
        or "não invente" in prompt.lower()
    ), "Prompt deve proibir inventar botões ou menus"


def test_prompt_no_ask_for_purchase_identification():
    """Regra 14: nunca pedir data, valor ou estabelecimento para identificar a compra."""
    prompt = _get_prompt()
    assert (
        "nunca peça" in prompt.lower()
        or "nunca pedir" in prompt.lower()
        or "já sabe qual" in prompt.lower()
    ), "Prompt deve proibir pedir dados de identificação da compra ao associado"


def test_prompt_short_responses():
    """Regra 15: respostas curtas, até 5 frases, sem tabelas."""
    prompt = _get_prompt()
    assert "5 frases" in prompt or "cinco frases" in prompt.lower(), (
        "Prompt deve limitar respostas a 5 frases"
    )
    assert "sem tabelas" in prompt.lower() or "tabelas" in prompt.lower(), (
        "Prompt deve proibir tabelas"
    )
