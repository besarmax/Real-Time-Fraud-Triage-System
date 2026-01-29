# 🛡️ Real-Time Fraud Triage System

![Python](https://img.shields.io/badge/Python-3.9-3776AB?style=flat&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EC2-232F3E?style=flat&logo=amazon-aws&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)

> **A containerized, cloud-deployed dashboard for monitoring high-risk financial transactions and triaging fraud in real-time.**

---

## 📖 Overview

The **Real-Time Fraud Triage System** is a full-stack data engineering project designed to simulate a financial monitoring environment. It ingests a stream of transactional data, processes it against a fraud detection logic layer, and visualizes flagged activities on a live dashboard for review.

The primary goal of this project was to build a robust, **containerized pipeline** that could be deployed to the cloud (AWS EC2) with a single command, demonstrating Infrastructure-as-Code principles and modern DevOps practices.

## 🏗️ Architecture

The system is composed of three Dockerized services orchestrated via `docker-compose`:

1.  **Database (PostgreSQL):** Persists transaction history and flagged events.
2.  **Fraud Engine (Python):** Generates synthetic transaction streams and applies heuristic rules (e.g., high-value anomalies, velocity checks) to flag suspicious activity.
3.  **Dashboard (Streamlit):** A low-latency frontend that allows analysts to view live transaction feeds and inspect flagged cases.

### Data Flow
`Synthetic Data Generator` $\rightarrow$ `Fraud Detection Logic` $\rightarrow$ `PostgreSQL DB` $\rightarrow$ `Streamlit Dashboard`

---

## 📸 Screenshots

### 1. The Triage Dashboard
*(Replace this text with a screenshot of your Streamlit app showing the table of transactions)*
![Dashboard View](screenshots/dashboard_view.png)
*Live view of incoming transactions with high-risk items highlighted in red.*

### 2. Infrastructure Setup
*(Replace this text with a screenshot of your VS Code terminal or AWS console)*
![System Architecture](screenshots/terminal_setup.png)
*Docker containers running the database and application services.*

---

## 🛠️ Tech Stack

* **Language:** Python 3.9
* **Database:** PostgreSQL
* **Containerization:** Docker & Docker Compose
* **Cloud Infrastructure:** AWS EC2 (t2.micro), Security Groups, IAM
* **Libraries:** `streamlit`, `pandas`, `psycopg2`, `sqlalchemy`, `faker`

---

## 🚀 How to Run Locally

Since the AWS demonstration instance has been terminated to prevent cost overruns, you can spin up the full environment locally using Docker.

### Prerequisites
* Docker Desktop installed
* Git installed

### Steps

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/your-username/fraud-triage-system.git](https://github.com/your-username/fraud-triage-system.git)
    cd fraud-triage-system
    ```

2.  **Configure Environment Variables**
    Create a `.env` file in the root directory. You can use the example provided:
    ```bash
    cp .env.example .env
    ```
    *Note: The `.env` file handles database credentials and configuration to ensure security best practices.*

3.  **Build and Run**
    Execute the Docker Compose command to build the images and start the network:
    ```bash
    docker-compose up --build
    ```

4.  **Access the Dashboard**
    Open your web browser and navigate to:
    `http://localhost:8501`

---

## 🧠 Key Learnings & Challenges

* **Container Orchestration:** Solved networking challenges between the Python application and the PostgreSQL container by utilizing Docker's internal DNS service discovery.
* **Cloud Security:** Configured AWS Security Groups to strictly limit inbound traffic, allowing access only on specific ports (SSH and Streamlit) while keeping the database port private.
* **State Management:** Implemented logic to handle "skip os shutdown" scenarios and data persistence using Docker Volumes.

## 🔮 Future Improvements

* **Machine Learning Integration:** Replace the heuristic rule-based detection with a trained `scikit-learn` Isolation Forest model for anomaly detection.
* **Alerting System:** Integrate AWS SNS (Simple Notification Service) to send SMS/Email alerts for transactions over $10,000.
* **CI/CD Pipeline:** Implement GitHub Actions to automatically lint code and build Docker images on push.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
