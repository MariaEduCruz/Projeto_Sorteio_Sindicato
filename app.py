# app.py - VERSÃO FINAL (planilha única + prêmio com imagem)

import os
import io
import sys
import uuid
import pandas as pd
from datetime import datetime
from flask import Flask, Response, jsonify, render_template, request


# Bloco de código para o PyInstaller encontrar as pastas
if getattr(sys, 'frozen', False):
    # se estiver rodando como um executável (.exe)
    base_path = sys._MEIPASS
    template_folder = os.path.join(base_path, 'templates')
    static_folder = os.path.join(base_path, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    # se estiver rodando como um script .py normal
    base_path = os.path.dirname(os.path.abspath(__file__))
    app = Flask(__name__)

# Pasta onde as imagens dos prêmios enviadas pelo operador serão salvas
PASTA_PREMIOS = os.path.join(app.static_folder, 'premios')
os.makedirs(PASTA_PREMIOS, exist_ok=True)

EXTENSOES_PERMITIDAS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}

# --- CONFIGURAÇÃO: AGORA APENAS UMA LISTA GERAL ---
dados_sorteio = {}

# Guarda o prêmio que está "selecionado" no momento pelo operador,
# antes de apertar o botão de sortear.
premio_atual = {
    'nome': '',
    'imagem': None  # caminho relativo, ex: /static/premios/uuid.png
}


def carregar_dados():
    try:
        csv_path = os.path.join(base_path, 'participantes_geral.csv')
        df = pd.read_csv(csv_path, dtype=str, encoding='utf-8')

        dados_sorteio['df_completo'] = df
        dados_sorteio['participantes_disponiveis'] = df.copy()
        dados_sorteio['total'] = len(df)
        dados_sorteio['historico'] = []
    except FileNotFoundError:
        print("AVISO: Arquivo 'participantes_geral.csv' não encontrado.")
        dados_sorteio['df_completo'] = pd.DataFrame(columns=['matricula', 'nome', 'cpf', 'celular'])
        dados_sorteio['participantes_disponiveis'] = pd.DataFrame(columns=['matricula', 'nome', 'cpf', 'celular'])
        dados_sorteio['total'] = 0
        dados_sorteio['historico'] = []


carregar_dados()

# --- ROTAS DO SITE ---

@app.route('/')
def tela_operador():
    """Renderiza a tela do operador com o histórico, participantes restantes, total e prêmio atual."""
    return render_template(
        'operador.html',
        dados={
            'restantes': len(dados_sorteio['participantes_disponiveis']),
            'total': dados_sorteio['total'],
            'historico': dados_sorteio['historico']
        },
        premio_atual=premio_atual
    )


@app.route('/telao')
def tela_publica():
    """Renderiza a tela pública do sorteio."""
    return render_template('publico.html')


@app.route('/definir-premio', methods=['POST'])
def definir_premio():
    """Recebe o nome do prêmio e, opcionalmente, uma imagem, e guarda como o prêmio atual."""
    nome = request.form.get('nome', '').strip()
    if not nome:
        nome = 'Brinde não especificado'

    arquivo = request.files.get('imagem')
    caminho_imagem = premio_atual['imagem']  # mantém a anterior se nenhuma nova for enviada

    if arquivo and arquivo.filename:
        extensao = os.path.splitext(arquivo.filename)[1].lower()
        if extensao not in EXTENSOES_PERMITIDAS:
            return jsonify({"erro": "Formato de imagem não suportado."}), 400

        nome_arquivo = f"{uuid.uuid4().hex}{extensao}"
        caminho_absoluto = os.path.join(PASTA_PREMIOS, nome_arquivo)
        arquivo.save(caminho_absoluto)
        caminho_imagem = f"/static/premios/{nome_arquivo}"

    premio_atual['nome'] = nome
    premio_atual['imagem'] = caminho_imagem

    return jsonify({"premio": premio_atual})


@app.route('/premio-atual')
def obter_premio_atual():
    """Permite que a tela pública consulte o prêmio selecionado no momento (ex: ao abrir a página)."""
    return jsonify({"premio": premio_atual})


@app.route('/sortear', methods=['POST'])
def sortear():
    """Realiza o sorteio de um participante e atualiza o histórico, vinculando ao prêmio atual."""
    if dados_sorteio['participantes_disponiveis'].empty:
        return jsonify({"erro": "Todos os participantes já foram sorteados!"}), 400

    sorteado_linha = dados_sorteio['participantes_disponiveis'].sample(n=1)
    indice_sorteado = sorteado_linha.index[0]
    dados_sorteio['participantes_disponiveis'] = dados_sorteio['participantes_disponiveis'].drop(indice_sorteado)

    sorteado_dados = sorteado_linha.to_dict(orient='records')[0]
    cpf_completo = sorteado_dados['cpf']
    sorteado_dados['cpf_publico'] = f"{cpf_completo[:3]}.***.***-{cpf_completo[-2:]}"

    premio_nome = premio_atual['nome'] or 'Brinde não especificado'
    premio_imagem = premio_atual['imagem']

    item_historico = {
        "nome": sorteado_dados['nome'],
        "matricula": sorteado_dados['matricula'],
        "premio": premio_nome,
        "premio_imagem": premio_imagem
    }
    dados_sorteio['historico'].append(item_historico)

    item_historico_texto = f"{item_historico['nome']} (Matrícula: {item_historico['matricula']}) - Prêmio: {item_historico['premio']}"

    resposta = {
        "sorteado": sorteado_dados,
        "premio": {
            "nome": premio_nome,
            "imagem": premio_imagem
        },
        "contagem": {
            "restantes": len(dados_sorteio['participantes_disponiveis']),
            "total": dados_sorteio['total']
        },
        "item_historico": item_historico_texto
    }
    return jsonify(resposta)


# Gerar Relatório
@app.route('/relatorio')
def gerar_relatorio():
    historico = dados_sorteio['historico']

    if not historico:
        return "Nenhum sorteio realizado para gerar relatório.", 404

    # Usa o Pandas para criar um DataFrame a partir do nosso histórico
    # (removemos a coluna do caminho da imagem, que não é útil no Excel)
    df_relatorio = pd.DataFrame(historico).drop(columns=['premio_imagem'], errors='ignore')

    # Prepara o nome do arquivo com data e hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"relatorio_sorteio_{timestamp}.xlsx"

    output = io.BytesIO()
    df_relatorio.to_excel(output, index=False, sheet_name='Sorteados')
    output.seek(0)

    # Cria e retorna a resposta que força o download no navegador
    return Response(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment;filename={nome_arquivo}"}
    )


# Inicia o servidor
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)