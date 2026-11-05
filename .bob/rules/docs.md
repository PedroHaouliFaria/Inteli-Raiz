# Regras de documentação (docs/)

## Escopo
Estas regras se aplicam a `docs/`, `README.md` da raiz e READMEs de pastas. Não mexa em `watson/` nem em código. As referências históricas de design ficam em `docs/anexos/experiencia-do-usuario/processo_design/`; preserve sua identificação como histórico e siga o escopo solicitado pelo usuário.

## Fontes da verdade
- Leitura principal: `docs/documentacao-do-projeto.md`. Atualize a história e a seção correspondente quando houver novas decisões ou resultados; use `docs/anexos/` para detalhes e fontes.
- Contrato da API: `docs/anexos/sistema/specs/contrato-da-api.md`. Não mude nome de campo, código de erro, status HTTP ou formato de resposta por conta própria. Se a spec estiver ambígua ou incompleta, pare e pergunte.
- Produto e regras: `docs/anexos/gestao/regras-do-produto.md`. Em caso de conflito entre código existente e o plano, vale o plano.
- Conteúdo das entregas D01–D13: `docs/anexos/gestao/guia-das-entregas.md`. Define estrutura, critério de conclusão e o que distingue aula, proposta interna e submissão.
- Em caso de conflito: o plano prevalece sobre o código; a spec prevalece sobre documentação antiga. Se ainda houver ambiguidade, pare e pergunte.

## Convenções de artefatos
- Cada Dxx deve ter: ID, versão/data, responsável por função, estado e origem.
- Estados distintos: revisão documental, teste automatizado, ensaio pela interface e validação com participantes. Não use um como substituto do outro.
- Os IDs `FON/HIP/DEC` e os prefixos `P1` e `P4-T` estão preservados porque já são citados no histórico. Não indicam separação de pastas por pessoa.
- Resultados reais vão para `docs/anexos/evidencias/` com versão, método e limite do experimento. Sem credenciais ou dados bancários identificáveis.

## Proibições
- Não criar falas, participantes, métricas de uso, capturas do Bob nem comprovantes de submissão.
- Não inventar datas, decisões ou estados que não foram registrados.
- Se algo não existe, documente a ausência e o próximo passo. Não preencha lacunas com suposições.

## Revisão cruzada
- Não marque como revisado por outra pessoa quando foi você quem escreveu ou consolidou o conteúdo. Outra pessoa deve revisar antes do encerramento de cada entrega.

## Idioma e nomenclatura
- Texto em português.
- Nomes descritivos em português, com palavras separadas por hífen. IDs D01–D13 ficam nos metadados, não nos nomes dos arquivos.
- Nomes de arquivos e pastas como já existem no repositório. Não renomeie sem pedido explícito.

## Forma de trabalhar
- Termine o que foi pedido e pare. Não adiante passos seguintes nem refatore documentos adjacentes sem solicitação.
- Antes de editar um documento, leia-o por inteiro para preservar o estilo, a estrutura e os IDs existentes.
- Não altere `.bobignore`.
