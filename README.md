[Leia em Português](README.pt-br.md)

# Advanced Raffle System for Union Events

A web application developed in Python with the Flask framework to conduct interactive and professional raffles. The system is designed for live events, featuring a comprehensive operator control panel and a dynamic public display screen.

## Key Features

-   **Dual Raffle System:** Manage two independent raffles simultaneously (e.g., a "General" raffle and a "Members Present" raffle), each with its own participant list, winner history, and counter.
-   **Prize Tracking:** Allows the operator to input the prize being drawn before each raffle, linking the winner to their specific prize.
-   **Downloadable XLSX Reports:** Generate and download professional, ready-to-use Excel (`.xlsx`) reports for each raffle type, containing the list of winners, their registration numbers, and the prizes they won.
-   **Operator Panel:** A comprehensive dashboard that displays the full details of the winner (Name, Registration, Phone), a running history of drawn participants, and a real-time counter.
-   **CPF Privacy:** The winner's CPF is masked by default on the operator panel, with a toggle button to reveal it when needed, ensuring data privacy.
-   **Public Display Screen:** A clean screen designed for projectors that shows the winner's name, registration, and a partially masked CPF for validation. It enhances the live event experience with a suspenseful drumroll sound, a pulsing "reveal" text, and a celebratory confetti animation.
-   **No-Repeat Guarantee:** The system ensures that a participant, once drawn, is removed from the pool and cannot be drawn again in the same session.

## Technologies Used

-   **Backend:** Python, Flask
-   **Data Handling:** Pandas, **OpenPyXL**
-   **Frontend:** HTML, CSS, JavaScript
-   **Animations & Effects:**
    -   `canvas-confetti` for the confetti effect.
    -   Custom CSS animations (`@keyframes`) for suspense effects.
-   **Development Tools:** Git, GitHub, Virtual Environments (`venv`).

## How to Set Up and Run the Project

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/MariaEduCruz/Projeto_Sorteio_Sindicato.git](https://github.com/MariaEduCruz/Projeto_Sorteio_Sindicato.git)
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd Projeto_Sorteio_Sindicato
    ```
3.  **Create the participant files:** Inside the main folder, create two CSV files with the same columns (`matricula,nome,cpf,celular`):
    -   `participantes_geral.csv`
    -   `participantes_presentes.csv`
4.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
5.  **Install the required dependencies from the `requirements.txt` file:**
    ```bash
    pip install -r requirements.txt
    pip install openpyxl
    ```
6.  **Run the application:**
    ```bash
    python app.py
    ```
7.  Open your browser and navigate to:
    -   **Operator Panel:** `http://127.0.0.1:5000/`
    -   **Public Display:** `http://127.0.0.1:5000/telao`