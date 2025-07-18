[Read in English](README.md)

# Raffle System for Union Members

This is a web application developed in Python using the Flask framework to conduct an interactive and professional raffle of registration numbers. The system features a control panel for the operator and a public display screen for the audience.

## Key Features

-   **Operator Panel:** A comprehensive dashboard that displays the full details of the winner (Name, Registration, CPF, Phone), a running history of drawn participants, and a real-time counter of remaining participants. It also includes controls to draw a new number and reset the entire raffle.
-   **Public Display Screen:** A clean screen designed for projectors that shows only the winner's name and registration number. It enhances the experience with a suspenseful drumroll sound, a pulsing "reveal" text, and a celebratory confetti animation.
-   **No-Repeat Guarantee:** The system ensures that a registration number, once drawn, is removed from the pool and cannot be drawn again in the same session.
-   **Dynamic Updates:** The operator's panel and public display are updated dynamically using JavaScript, without needing page reloads.

## Technologies Used

-   **Backend:** Python, Flask
-   **Data Handling:** Pandas
-   **Frontend:** HTML, CSS, JavaScript
-   **Animations & Effects:**
    -   `canvas-confetti` for the confetti effect.
    -   Custom CSS animations (`@keyframes`) for suspense effects.
-   **Development Tools:** Git, GitHub, Virtual Environments (`venv`).

## How to Set Up and Run the Project

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/MariaEduCruz/sorteio-sindicato.git](https://github.com/MariaEduCruz/sorteio-sindicato.git)
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd projeto-sorteio-sindicato
    ```
3.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
4.  **Install the required dependencies from the `requirements.txt` file:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run the application:**
    ```bash
    python app.py
    ```
6.  Open your browser and navigate to:
    -   **Operator Panel:** `http://127.0.0.1:5000/`
    -   **Public Display:** `http://127.0.0.1:5000/telao`
