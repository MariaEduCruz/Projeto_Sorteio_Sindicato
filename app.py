# app.py - VERSÃO FINAL

import pandas as pd
from flask import Flask, jsonify, render_template

app = Flask(__name__)

try:
    df_completo = pd.read_csv('participantes.csv', dtype=str)
except FileNotFoundError:
    print("ERRO: Arquivo 'participantes.csv' não foi encontrado!")
    df_completo = pd.DataFrame(columns=['matricula', 'nome', 'cpf', 'celular'])

participantes_disponiveis = df_completo.copy()

total_participantes = len(df_completo)

historico_sorteados = []


# --- ROTAS DO SITE ---

@app.route('/')
def tela_operador():
    """Renderiza a tela do operador com o histórico, participantes restantes e total."""
    return render_template(
        'operador.html', 
        historico=historico_sorteados,
        restantes=len(participantes_disponiveis),
        total=total_participantes
    )

@app.route('/telao')
def tela_publica():
    """Renderiza a tela pública do sorteio."""
    return render_template('publico.html')

@app.route('/sortear', methods=['POST'])
def sortear():
    """Realiza o sorteio de um participante e atualiza o histórico."""
    global participantes_disponiveis
    global historico_sorteados

    if not participantes_disponiveis.empty:
        sorteado_linha = participantes_disponiveis.sample(n=1)
        indice_sorteado = sorteado_linha.index[0]
        participantes_disponiveis = participantes_disponiveis.drop(indice_sorteado)
        sorteado_dados = sorteado_linha.to_dict(orient='records')[0]
        
        item_historico = f"{sorteado_dados['nome']} (Matrícula: {sorteado_dados['matricula']})"
        historico_sorteados.append(item_historico)
    
        resposta = {
            "sorteado": sorteado_dados,
            "contagem": {
                "restantes": len(participantes_disponiveis),
                "total": total_participantes
            },
            "item_historico": item_historico
        }
        
        return jsonify(resposta)
    else:
        return jsonify({"erro": "Todos os participantes já foram sorteados!"}), 400

# Inicia o servidor
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)