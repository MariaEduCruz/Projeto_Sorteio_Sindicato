[Leia em Português](README.pt-br.md)

# Sistema de Sorteio para Sindicato

Aplicação web desenvolvida em Python com o framework Flask para realizar sorteios de matrículas de forma interativa e profissional. O sistema conta com um painel de controle para o operador e uma tela de exibição pública para a audiência.

## Principais Funcionalidades

-   **Painel do Operador:** Um dashboard completo que exibe os dados detalhados do sorteado (Nome, Matrícula, CPF, Celular), um histórico dos participantes já sorteados e um contador em tempo real dos participantes restantes. Inclui controles para sortear um novo número e para reiniciar o sorteio completamente.
-   **Tela Pública (Telão):** Uma tela limpa, projetada para telões, que mostra apenas o nome e a matrícula do ganhador. A experiência é enriquecida com um som de rufar de tambores para suspense, texto pulsante e uma animação de confetes para a celebração.
-   **Garantia de Não Repetição:** O sistema assegura que uma matrícula, uma vez sorteada, é removida da lista e não pode ser sorteada novamente na mesma sessão.
-   **Atualizações Dinâmicas:** O painel do operador e a tela pública são atualizados dinamicamente com JavaScript, sem a necessidade de recarregar a página.

## Tecnologias Utilizadas

-   **Backend:** Python, Flask
-   **Manipulação de Dados:** Pandas
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
3.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
4.  **Instale as dependências necessárias a partir do arquivo `requirements.txt`:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Execute a aplicação:**
    ```bash
    python app.py
    ```
6.  Abra seu navegador e acesse:
    -   **Painel do Operador:** `http://127.0.0.1:5000/`
    -   **Tela Pública:** `http://127.0.0.1:5000/telao`
