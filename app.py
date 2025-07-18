# app.py - VERSÃO FINAL E CORRIGIDA

import pandas as pd
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# --- CONFIGURAÇÃO INICIAL ---
# Estas variáveis são lidas apenas uma vez, quando o servidor inicia.

try:
    # Carrega a lista completa de participantes do arquivo CSV.
    df_completo = pd.read_csv('participantes.csv', dtype=str)
except FileNotFoundError:
    print("ERRO: Arquivo 'participantes.csv' não foi encontrado!")
    df_completo = pd.DataFrame(columns=['matricula', 'nome', 'cpf', 'celular'])

# Faz uma cópia da lista completa para ser a nossa lista de "disponíveis".
# É desta lista que vamos remover os sorteados.
participantes_disponiveis = df_completo.copy()

# Guarda o número total de participantes para o nosso contador.
total_participantes = len(df_completo)

# Cria a lista vazia que vai armazenar o histórico dos nomes sorteados.
historico_sorteados = []


# --- ROTAS DO SITE ---

# Rota principal: a tela do operador
@app.route('/')
def tela_operador():
    # A cada vez que a página do operador é carregada, nós enviamos para ela:
    # 1. A lista atualizada do histórico.
    # 2. O número de participantes que ainda podem ser sorteados.
    # 3. O número total de participantes do início.
    return render_template(
        'operador.html', 
        historico=historico_sorteados,
        restantes=len(participantes_disponiveis),
        total=total_participantes
    )

# Rota da tela pública
@app.route('/telao')
def tela_publica():
    return render_template('publico.html')

# Rota da API que faz a mágica do sorteio
# Substitua a sua função sortear() antiga por esta:

@app.route('/sortear', methods=['POST'])
def sortear():
    global participantes_disponiveis
    global historico_sorteados

    if not participantes_disponiveis.empty:
        sorteado_linha = participantes_disponiveis.sample(n=1)
        indice_sorteado = sorteado_linha.index[0]
        participantes_disponiveis = participantes_disponiveis.drop(indice_sorteado)
        sorteado_dados = sorteado_linha.to_dict(orient='records')[0]
        
        # Adiciona o nome e a matrícula ao histórico
        item_historico = f"{sorteado_dados['nome']} (Matrícula: {sorteado_dados['matricula']})"
        historico_sorteados.append(item_historico)
        
        # MUDANÇA PRINCIPAL: Criamos uma resposta completa em formato JSON
        # Agora, além dos dados do sorteado, enviamos também a nova contagem
        # e o item exato que deve ser adicionado ao histórico.
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

# NOVA ROTA PARA REINICIAR O SORTEIO
@app.route('/reiniciar', methods=['POST'])
def reiniciar_sorteio():
    global participantes_disponiveis
    global historico_sorteados

    # Restaura a lista de disponíveis para a lista completa original
    participantes_disponiveis = df_completo.copy()
    
    # Limpa a lista de histórico dos sorteados
    historico_sorteados.clear() # .clear() é uma forma eficiente de esvaziar a lista

    # Retorna uma mensagem de sucesso para o JavaScript
    return jsonify({"status": "ok", "mensagem": "Sorteio reiniciado com sucesso!"})

# A linha abaixo deve continuar sendo a última do arquivo
if __name__ == '__main__':
    app.run(debug=True) 

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)