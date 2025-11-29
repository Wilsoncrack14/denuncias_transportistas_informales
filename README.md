# Denuncias Policiales

Welcome to the **Denuncias Policiales** project. This is a full-stack web application designed to manage and process police reports efficiently.

## 🚀 Tech Stack

This project utilizes a modern technology stack:

- **Backend**: Django (Python)
- **Frontend**: Node.js
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## 🛠️ Installation & Setup

Follow these steps to get the project up and running locally:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd denuncias-policiales
   ```

2. **Start the application:**
   Use Docker Compose to build and start the services.
   ```bash
   docker-compose up --build
   ```

   This command will start:
   - **Backend** on port `8000`
   - **Frontend** on port `3000`
   - **Database** (PostgreSQL) on port `5432`

3. **Access the application:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)

## 📂 Project Structure

The project is organized into the following main directories:

- **`server-side/`**: Contains the Node.js frontend application source code.
- **`services/`**: Contains the Django backend application source code, including apps for:
    - `auth_service`
    - `chat_service`
    - `dashboard_service`
    - `denuncias_service`
    - `users_service`

## ⚙️ Configuration

The application uses `docker-compose.yml` for orchestration.
- **Database**: Configured with default credentials (`postgres`/`postgres`) and database name `app_dev`.
- **Volumes**: Source code is mounted into containers for development convenience (`./services:/app` and `./server-side:/app`).

## 🤝 Contributing

We welcome contributions! Please check the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## 📄 License

[License Information Here]
