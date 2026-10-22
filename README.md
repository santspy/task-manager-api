<img width="1920" height="950" alt="{8ACFD479-92C5-4396-B983-6555ABB4A1C4}" src="https://github.com/user-attachments/assets/9559f7cf-5f62-4cb9-9d6f-d175f626f722" />
<img width="503" height="444" alt="{4DB64C1A-F9DD-4102-9248-1C7C11CFDA05}" src="https://github.com/user-attachments/assets/9015ad04-09bb-4a51-879a-e8278386b3e8" />
<img width="503" height="444" alt="{0067298E-FD8F-470B-AC33-A186F688960A}" src="https://github.com/user-attachments/assets/3d2397d8-746a-480f-a3a9-8c74e18072e0" />
<img width="1024" height="169" alt="{4AD1141A-9680-46BC-BD31-15BFC022F6B1}" src="https://github.com/user-attachments/assets/747a4fbc-d206-4b2f-bfcb-22f2d01ac156" />
<img width="1024" height="169" alt="{2CD02CD1-67AE-4EC6-9769-F3D8B5E5C104}" src="https://github.com/user-attachments/assets/17d5bbc7-a6f3-4e16-aaeb-cb271a74e33a" />
<img width="1024" height="169" alt="{2943329A-E0BF-418F-B7ED-FFE38AB57F81}" src="https://github.com/user-attachments/assets/6312a5f6-277c-41a1-a66d-98fc9b3450bb" />
<img width="1381" height="253" alt="{7BC0751E-8ED8-43B2-9A43-51B854ECEE1F}" src="https://github.com/user-attachments/assets/a679cc67-95c7-43d7-9448-408e88eb53d8" />



#Task Manager API



A backend REST API built with FastAPI, PostgreSQL and SQLAlchemy, featuring JWT authentication, automated tests, Docker and Kubernetes configuration.



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


| GET | / | Welcome root message | No |

| POST | /register | Register a new user | No |

| POST | /token | Authenticate and obtain JWT Bearer Token | No |

| POST | /tasks/ | Create a new task | Yes |

| GET | /tasks/ | Retrieve tasks owned by current user | Yes |



---



##License



This project is licensed under the MIT License. Feel free to use and contribute!
