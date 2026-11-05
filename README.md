# Inteli-Raiz

Projeto da optativa IBM do Inteli: confirmação assistida de compras pelo associado, com dados sintéticos e ações financeiras simuladas.

## Objetivo do projeto

Ajudar o associado do Sicredi a entender uma compra suspeita e decidir se reconhece e autoriza, não reconhece ou está em dúvida.

O sistema apresenta a compra; o assistente de IA consulta os dados disponíveis para esclarecer dúvidas; o associado escolhe uma resposta; o sistema registra o resultado e encaminha exceções para uma pessoa analisar. A IA não autoriza compras pelo associado.

Queremos verificar se essa ajuda melhora a compreensão do alerta e do próximo passo. O protótipo usa dados sintéticos e operações simuladas; a melhoria da experiência ainda precisa ser testada com pessoas.

## Comece aqui

1. **[Leia a documentação do projeto](docs/documentacao-do-projeto.md):** história, persona, decisões, custos de mercado, dados, construção e resultados.
2. [Use a demonstração](docs/anexos/sistema/como-usar-a-demonstracao.md): instalação e passo a passo.
3. [Consulte os anexos](docs/anexos/README.md): contratos, dados, evidências e planos históricos.
4. [Veja o que falta concluir](docs/anexos/gestao/o-que-falta-concluir.md).

Os arquivos `.md` são documentos de texto em Markdown. Clique no arquivo no GitHub para ler a versão formatada. `README.md` funciona como página inicial.

## Estrutura

```text
docs/
  documentacao-do-projeto.md  explicação completa do projeto
  anexos/                    fontes, detalhes técnicos e registros históricos
watson/            código da aplicação e infraestrutura
data/              orientações, dicionário e bases processadas
notebooks/         análise, preparação e avaliação do modelo
scripts/           rotinas auxiliares
outputs/           resultados e modelo serializado
contexto/          materiais do programa IBM
bob_sessions/      evidências reais de uso do IBM Bob
```

A consolidação documental não equivale a teste com usuários. Backend reproduzido; LLM externo real, ensaio independente pela interface e validação de experiência têm pendências registradas em [critérios e pendências](docs/anexos/gestao/o-que-falta-concluir.md).
