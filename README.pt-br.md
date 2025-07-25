[Read in English](README.md)

# Sistema Avançado de Sorteio para Eventos de Sindicato

Aplicação web desenvolvida em Python com o framework Flask para realizar sorteios de matrículas de forma interativa e profissional. O sistema é projetado para eventos ao vivo, contando com um painel de controle completo para o operador e uma tela de exibição pública dinâmica para a audiência.

## Principais Funcionalidades

-   **Sistema de Sorteio Duplo:** Gerencie dois sorteios independentes simultaneamente (ex: um sorteio "Geral" e um de "Presentes"), cada um com sua própria lista de participantes, histórico de vencedores e contador.
-   **Registro de Prêmios:** Permite que o operador insira o prêmio que está sendo sorteado antes de cada rodada, vinculando o ganhador ao seu prêmio específico.
-   **Relatórios em Excel (XLSX):** Gere e baixe relatórios profissionais em formato Excel (`.xlsx`), prontos para uso, para cada tipo de sorteio, contendo a lista de ganhadores, suas matrículas e os prêmios que ganharam.
-   **Painel do Operador:** Um dashboard completo que exibe os dados detalhados do sorteado (Nome, Matrícula, Celular), um histórico dos participantes já sorteados e um contador em tempo real.
-   **Privacidade de CPF:** O CPF do ganhador é exibido mascarado por padrão no painel do operador, com um botão para revelar quando necessário, garantindo a privacidade dos dados.
-   **Tela Pública (Telão):** Uma tela limpa, projetada para telões, que mostra o nome, a matrícula e um CPF parcialmente mascarado do ganhador para validação. A experiência do evento é enriquecida com um som de rufar de tambores para suspense, texto pulsante e uma animação de confetes para a celebração.
-   **Garantia de Não Repetição:** O sistema assegura que um participante, uma vez sorteado, é removido da lista e não pode ser sorteado novamente na mesma sessão.

## Tecnologias Utilizadas

-   **Backend:** Python, Flask
-   **Manipulação de Dados:** Pandas, **OpenPyXL**
-   **Frontend:** HTML, CSS, JavaScript
-   **Animações e Efeitos:**
    -   `canvas-confetti` para o efeito de confetes.
    -   Animações customizadas em CSS (`@keyframes`) para os efeitos de suspense.
-   **Ferramentas de Desenvolvimento:** Git, GitHub, Ambientes Virtuais (`venv`).

## Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/MariaEduCruz/Projeto_Sorteio_Sindicato.git
    ```
2.  **Navegue até o diretório do projeto:**
    ```bash
    cd Projeto_Sorteio_Sindicato
    ```
3.  **Crie os arquivos de participantes:** Dentro da pasta principal, crie dois arquivos CSV com as mesmas colunas (`matricula,nome,cpf,celular`):
    -   `participantes_geral.csv`
    -   `participantes_presentes.csv`
4.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
5.  **Instale as dependências necessárias a partir do arquivo `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    pip install openpyxl
    ```
6.  **Execute a aplicação:**
    ```bash
    python app.py
    ```
7.  Abra seu navegador e acesse:
    -   **Painel do Operador:** `http://12-7.0.0.1:5000/`
    -   **Tela Pública:** `http://127.0.0.1:5000/telao`