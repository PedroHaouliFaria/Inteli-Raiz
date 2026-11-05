"""Recalcula o orcamento da documentacao, sem rede e sem credenciais.

python3 scripts/calcular_custos_projeto.py          # tabela em Markdown
python3 scripts/calcular_custos_projeto.py --check  # confere a tabela publicada
"""
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
PREMISSAS = ROOT / 'docs/anexos/gestao/premissas-financeiras.json'
DOCUMENTO = ROOT / 'docs/documentacao-do-projeto.md'
INICIO = '<!-- custos-calculados:inicio -->'
FIM = '<!-- custos-calculados:fim -->'


def decimal(value):
    return Decimal(str(value))


def reais(value):
    rounded = value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return 'R$ ' + f'{rounded:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def calcular(data):
    p, h = data['precos'], data['hipoteses']
    fx = decimal(p['usd_brl'])
    fator = decimal(h['fator_custo_pessoal'])
    horas = decimal(h['horas_produtivas_mes'])
    atendimento_hora = decimal(p['salario_atendimento_brl_mes']) * fator / horas
    desenvolvimento_hora = decimal(p['salario_desenvolvimento_brl_mes']) * fator / horas
    infra = decimal(p['vm_usd_mes']) * (1 + decimal(p['backup_fracao_vm'])) * fx
    manutencao = decimal(h['manutencao_horas_mes']) * desenvolvimento_hora
    bob_mensal = decimal(p['bob_pro_usd_usuario_mes']) * decimal(h['bob_usuarios_manutencao']) * fx
    bob_construcao = decimal(p['bob_pro_usd_usuario_mes']) * decimal(h['bob_usuarios_construcao']) * decimal(h['bob_meses_construcao']) * fx
    construcao = decimal(h['construcao_horas_referencia']) * desenvolvimento_hora + bob_construcao
    cenarios = []
    for c in data['cenarios']:
        n = decimal(c['confirmacoes_mes'])
        chamadas = n * decimal(c['fracao_chat']) * decimal(c['chamadas_sessao'])
        entrada = chamadas * decimal(c['tokens_entrada_chamada'])
        saida = chamadas * decimal(c['tokens_saida_chamada'])
        llm_usd = (entrada * decimal(p['llm_usd_milhao_entrada']) + saida * decimal(p['llm_usd_milhao_saida'])) / 1_000_000
        llm = llm_usd * fx
        horas_revisao = n * decimal(c['fracao_revisao']) * decimal(c['minutos_revisao']) / 60
        humano = horas_revisao * atendimento_hora
        tecnologia = infra + llm
        total = tecnologia + humano + manutencao + bob_mensal
        cenarios.append(dict(nome=c['nome'], n=n, chamadas=chamadas, entrada=entrada, saida=saida, llm=llm, humano=humano, tecnologia=tecnologia, total=total, unitario=total/n))
    return dict(cenarios=cenarios, infra=infra, manutencao=manutencao, bob_mensal=bob_mensal,
                bob_construcao=bob_construcao, construcao=construcao,
                atendimento_hora=atendimento_hora, desenvolvimento_hora=desenvolvimento_hora)


def tabela(data):
    r = calcular(data)
    lines = ['| Custo mensal de referência | Base | Uso intenso | Contexto longo |', '|---|---:|---:|---:|']
    for label, values in [
        ('Hospedagem e backup', [r['infra']]*3),
        ('IA por consumo', [c['llm'] for c in r['cenarios']]),
        ('Subtotal de tecnologia', [c['tecnologia'] for c in r['cenarios']]),
        ('Tempo humano de revisão (custo alocado)', [c['humano'] for c in r['cenarios']]),
        ('Manutenção técnica: 4 h/mês (hipótese)', [r['manutencao']]*3),
        ('Bob Pro: 1 usuário na manutenção (hipótese)', [r['bob_mensal']]*3),
        ('Total mensal estimado', [c['total'] for c in r['cenarios']]),
        ('Custo alocado por confirmação', [c['unitario'] for c in r['cenarios']]),
    ]:
        lines.append('| '+label+' | '+' | '.join(reais(v) for v in values)+' |')
    return '\n'.join(lines)


def main():
    data = json.loads(PREMISSAS.read_text())
    rendered = tabela(data)
    if '--check' in sys.argv:
        text = DOCUMENTO.read_text()
        published = text.split(INICIO, 1)[1].split(FIM, 1)[0].strip()
        if published != rendered:
            raise SystemExit('A tabela publicada diverge das premissas. Recalcule antes de alterar.')
        print('Tabela financeira confere com preços, premissas e fórmulas.')
    else:
        print(rendered)


if __name__ == '__main__':
    main()
