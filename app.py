# app.py - VERSÃO FINAL

import os
import sys
import pandas as pd
from flask import Flask, jsonify, render_template, request


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

# --- CONFIGURAÇÃO PARA DUAS LISTAS ---
dados_sorteio = {
    'geral': {},
    'presentes': {}
}

def carregar_dados(tipo):
    try:
        csv_path = os.path.join(base_path, f'participantes_{tipo}.csv')
        df = pd.read_csv(csv_path, dtype=str, encoding='utf-8')

        dados_sorteio[tipo]['df_completo'] = df
        dados_sorteio[tipo]['participantes_disponiveis'] = df.copy()
        dados_sorteio[tipo]['total'] = len(df)
        dados_sorteio[tipo]['historico'] = []
    except FileNotFoundError:
        print(f"AVISO: Arquivo 'participantes_{tipo}.csv' não encontrado.")
        dados_sorteio[tipo]['df_completo'] = pd.DataFrame(columns=['matricula', 'nome', 'cpf', 'celular'])
        dados_sorteio[tipo]['participantes_disponiveis'] = pd.DataFrame(columns=['matricula', 'nome', 'cpf', 'celular'])
        dados_sorteio[tipo]['total'] = 0
        dados_sorteio[tipo]['historico'] = []

carregar_dados('geral')
carregar_dados('presentes')

# --- ROTAS DO SITE ---

@app.route('/')
def tela_operador():
    """Renderiza a tela do operador com o histórico, participantes restantes e total."""
    return render_template(
        'operador.html', 
        dados_geral={'restantes': len(dados_sorteio['geral']['participantes_disponiveis']), 'total': dados_sorteio['geral']['total'], 'historico': dados_sorteio['geral']['historico']},
        dados_presentes={'restantes': len(dados_sorteio['presentes']['participantes_disponiveis']), 'total': dados_sorteio['presentes']['total'], 'historico': dados_sorteio['presentes']['historico']}
    )

@app.route('/telao')
def tela_publica():
    """Renderiza a tela pública do sorteio."""
    return render_template('publico.html')

@app.route('/sortear', methods=['POST'])
def sortear():
    """Realiza o sorteio de um participante e atualiza o histórico."""
    tipo_sorteio = request.args.get('tipo', 'geral')
    if tipo_sorteio not in dados_sorteio:
        return jsonify({"erro": "Tipo de sorteio inválido."}), 400

    sorteio_atual = dados_sorteio[tipo_sorteio]

    if not sorteio_atual['participantes_disponiveis'].empty:
        sorteado_linha = sorteio_atual['participantes_disponiveis'].sample(n=1)
        indice_sorteado = sorteado_linha.index[0]
        sorteio_atual['participantes_disponiveis'] = sorteio_atual['participantes_disponiveis'].drop(indice_sorteado)
        
        sorteado_dados = sorteado_linha.to_dict(orient='records')[0]
        cpf_completo = sorteado_dados['cpf']
        sorteado_dados['cpf_publico'] = f"{cpf_completo[:3]}.***.***-{cpf_completo[-2:]}"
        
        item_historico = f"{sorteado_dados['nome']} (Matrícula: {sorteado_dados['matricula']})"
        sorteio_atual['historico'].append(item_historico)
        
        resposta = {
            "sorteado": sorteado_dados,
            "contagem": {
                "restantes": len(sorteio_atual['participantes_disponiveis']),
                "total": sorteio_atual['total']
            },
            "item_historico": item_historico
        }
        return jsonify(resposta)
    else:
        return jsonify({"erro": f"Todos os participantes do sorteio '{tipo_sorteio}' já foram sorteados!"}), 400

# Inicia o servidor
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)