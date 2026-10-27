"""
Publica outputs/modelo_rf.joblib no watsonx.ai Runtime como deploy online.

Variáveis de ambiente:
  WML_API_KEY   API key da IBM Cloud de um membro do deployment space
  WML_SPACE_ID  ID do deployment space (Deployments → space → Manage → Space GUID)
  WML_URL       opcional; padrão https://us-south.ml.cloud.ibm.com (Dallas)

Rode com o venv do notebook 03 (Python 3.12, scikit-learn 1.6, pandas 2.2):
  python scripts/deploy_watsonx.py
"""

import functools
import os
from pathlib import Path

import httpx
import joblib
from ibm_watsonx_ai import APIClient, Credentials

# O ibm-watsonx-ai 1.8.1 sobe o conteúdo do modelo com httpx.put sem timeout,
# então vale o padrão de 5 s do httpx e o upload falha com ReadTimeout.
httpx.put = functools.partial(httpx.put, timeout=300)

ROOT = Path(__file__).resolve().parent.parent
CAMINHO_MODELO = ROOT / "outputs" / "modelo_rf.joblib"

NOME = "rf_fraude_sicredi"
MODEL_TYPE = "scikit-learn_1.6"
SOFTWARE_SPEC = "runtime-25.1-py3.12"


def main() -> None:
    credenciais = Credentials(
        url=os.environ.get("WML_URL", "https://us-south.ml.cloud.ibm.com"),
        api_key=os.environ["WML_API_KEY"],
    )
    client = APIClient(credenciais, space_id=os.environ["WML_SPACE_ID"])

    # O deploy exige uma task credential na conta; sem ela a API devolve
    # missing_user_task_credential. Cria uma com a API key atual se faltar.
    if not client.task_credentials.get_details()["resources"]:
        client.task_credentials.store(name="inteli-raiz deploy")

    # Reaproveita o modelo se uma execução anterior já o publicou.
    existentes = [
        r["metadata"]["id"]
        for r in client.repository.get_model_details()["resources"]
        if r["metadata"]["name"] == NOME
    ]
    if existentes:
        model_id = existentes[0]
    else:
        # Arquivo gerado pelo próprio notebook 03, não por terceiros.
        modelo = joblib.load(CAMINHO_MODELO)
        sw_spec_id = client.software_specifications.get_id_by_name(SOFTWARE_SPEC)
        publicado = client.repository.store_model(
            model=modelo,
            meta_props={
                client.repository.ModelMetaNames.NAME: NOME,
                client.repository.ModelMetaNames.TYPE: MODEL_TYPE,
                client.repository.ModelMetaNames.SOFTWARE_SPEC_ID: sw_spec_id,
            },
        )
        model_id = client.repository.get_model_id(publicado)
    print(f"model_id={model_id}")

    deploy = client.deployments.create(
        model_id,
        meta_props={
            client.deployments.ConfigurationMetaNames.NAME: f"{NOME}_online",
            client.deployments.ConfigurationMetaNames.ONLINE: {},
        },
    )
    print(f"deployment_id={client.deployments.get_id(deploy)}")


if __name__ == "__main__":
    main()
