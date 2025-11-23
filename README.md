# Reservoir Engineering REST API

A comprehensive backend solution for managing oil & gas reservoir data, developed using **Python (Flask)** and **PostgreSQL**.

## 🚀 Features

* **CRUD Operations:** Manage well headers and production data securely.
* **Data Engineering (ETL):** Pipelines to process bulk Excel production data.
* **Engineering Calculations:** Automated analysis for GOR (Gas Oil Ratio) and Water Cut.
* **Visualization:** On-the-fly generation of production plots using Matplotlib.
* **Containerization:** Fully Dockerized application (Web + DB) using Docker Compose.
* **Testing:** Automated integration tests using `pytest`.

## 🛠️ Tech Stack

* **Language:** Python 3.9
* **Framework:** Flask (Modular Architecture with Blueprints)
* **Database:** PostgreSQL 14
* **ORM:** SQLAlchemy
* **Data Processing:** Pandas, NumPy
* **DevOps:** Docker, Docker Compose, GitHub Actions (CI/CD)

## 📦 How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/tohidsami/reservoir-backend.git](https://github.com/tohidsami/reservoir-backend.git)
    cd reservoir-backend
    ```

2.  **Run with Docker (Recommended):**
    ```bash
    docker-compose up --build
    ```

3.  **Access the API:**
    * List wells: `http://localhost:5000/api/wells`
    * Plot data: `http://localhost:5000/api/wells/1/plot`

## 🧪 Running Tests

Execute the test suite inside the container:
```bash
docker exec -it <container_name> pytest -v