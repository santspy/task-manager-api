#Task Manager API



A professional, production-ready RESTful API built with FastAPI, SQLAlchemy, and PostgreSQL, featuring JWT (JSON Web Tokens) authentication and an automated testing suite using pytest.



---



##Tech Stack



* Language: Python 3.11+

* Framework: FastAPI (https://fastapi.tiangolo.com/)

* ORM: SQLAlchemy (https://www.sqlalchemy.org/)

* Database: PostgreSQL

* Authentication: JWT (python-jose) + Hashing via bcrypt

* Automated Testing: pytest & httpx

* Containerization: Docker & Docker Compose



---



##Repository Structure



task-manager-api/

├── app.py              # Application entry point (routes, models, auth)

├── requirements.txt    # Project dependencies

├── .gitignore          # Git exclusion rules

├── tests/

│   └── test_api.py     # Automated unit & integration tests

└── README.md           # Project documentation



---



##Getting Started (Local Setup)



###Prerequisites



* Python 3.11 or higher

* A running instance of PostgreSQL (local or cloud)



###1. Clone the Repository



git clone https://github.com/santspy/task-manager-api.git

cd task-manager-api



###2. Set Up a Virtual Environment



* Windows (PowerShell):

  python -m venv .venv

  .\.venv\Scripts\Activate.ps1



* Linux / macOS:

  python3 -m venv .venv

  source .venv/bin/activate



###3. Install Dependencies



pip install --upgrade pip

pip install --only-binary=:all: --prefer-binary -r requirements.txt



###4. Configure Environment Variables (Optional)



By default, the application connects to a local PostgreSQL database at localhost:5432 with user postgres and password postgres. Override these defaults by setting environment variables:



export DB_USER=your_user

export DB_PASSWORD=your_password

export DB_HOST=localhost

export DB_NAME=tasks_db



###5. Run the Development Server



uvicorn app:app --reload



Access the interactive API documentation in your browser:

* Swagger UI: http://127.0.0.1:8000/docs

* ReDoc: http://127.0.0.1:8000/redoc



---



##Running Automated Tests



The test suite uses pytest to validate authentication workflows and API endpoints.



Ensure your virtual environment is active, then run:



* Windows (PowerShell):

  $env:PYTHONPATH="."

  pytest -v



* Linux / macOS:

  PYTHONPATH=. pytest -v



---



##Running with Docker (Optional)



To spin up both the API and the PostgreSQL database in isolated containers:



### 1. Start the Containers



docker compose up -d --build



### 2. View Application Logs



docker compose logs -f



### 3. Stop the Containers



docker compose down



---



##Key API Endpoints



| Method | Endpoint | Description | Requires Auth? |

| :--- | :--- | :--- | :---: |

| GET | / | Welcome root message | No |

| POST | /register | Register a new user | No |

| POST | /token | Authenticate and obtain JWT Bearer Token | No |

| POST | /tasks/ | Create a new task | Yes |

| GET | /tasks/ | Retrieve tasks owned by current user | Yes |



---



##License



This project is licensed under the MIT License. Feel free to use and contribute!
