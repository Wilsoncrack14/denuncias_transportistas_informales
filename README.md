# Denuncias Policiales

Welcome to the **Denuncias Policiales** project. This is a full-stack web application designed to manage and process police reports efficiently.

## 🚀 Tech Stack

This project utilizes a modern technology stack:

- **Backend**: Django (Python) - Modular Monolith
- **Microservices**: FastAPI (Python) - Notification Service
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

2. **Configure Environment Variables:**

   **Backend (`services/`):**
   - Create a `.env` file in `services/`.
   - Add your API keys (e.g., for DNI validation):
     ```env
     API_KEY=your_apisperu_token
     ```

   **Notification Service (`notification_service/`):**
   - Create a `.env` file in `notification_service/`.
   - Add your Brevo (Sendinblue) credentials:
     ```env
     BREVO_SMTP_SERVER=smtp-relay.brevo.com
     BREVO_PORT=587
     BREVO_LOGIN=your_email@example.com
     BREVO_PASSWORD=your_smtp_key
     SENDER_EMAIL=no-reply@denuncias-policiales.com
     ```

3. **Start the application:**
   Use Docker Compose to build and start the services.
   ```bash
   docker-compose up --build
   ```

   This command will start:
   - **Backend** on port `8000`
   - **Notification Service** on port `8001`
   - **Frontend** on port `3000`
   - **Database** (PostgreSQL) on port `5432`

4. **Access the application:**
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **Backend Admin**: [http://localhost:8000/admin](http://localhost:8000/admin)
   - **API Documentation**: [http://localhost:8000/api/docs](http://localhost:8000/api/docs) (if configured)

## 🔑 Default Credentials

A superuser is available for initial access:
- **Email**: `admin_usb@example.com`
- **Password**: `password123`
- **DNI**: `87654321`

## 📂 Project Structure

The project is organized into the following main directories:

- **`server-side/`**: Node.js frontend application.
- **`services/`**: Django backend (Auth, Denuncias, Users).
- **`notification_service/`**: FastAPI microservice for email notifications.
- **`postgres_data/`**: Local folder for database persistence (ignored by Git).

## ✨ Key Features

- **User Management**: Registration, Login, DNI Validation.
- **Denuncias**: Create, View, and Track police reports.
- **Notifications**:
    - **Welcome Email**: Sent upon registration.
    - **Status Updates**: Sent when a report status changes (e.g., Pending -> In Progress).
- **Role-Based Access**:
    - **Citizens**: Manage their own reports.
    - **Authorities (Superusers)**: View heatmap, manage all users, and update report statuses.

## ⚙️ Configuration

- **Database Persistence**: Data is saved in the local `postgres_data/` folder, making it easy to transport the project on a USB drive.
- **Microservices Communication**: The Django backend communicates with the Notification Service via HTTP requests within the Docker network.

## 🤝 Contributing

We welcome contributions! Please check the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.
