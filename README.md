# task manager API - secured & containerized

welcome! This repository contains a production-ready **task manager API** built with **fastAPI** and **postgreSQL**. 

the goal of this project was to go beyond a simple CRUD application by implementing secure JWT authentication, strict user data isolation, and taking the application through the full DevOps lifecycle—from local multi-container development with Docker to orchestration on a local **Kubernetes** cluster.

---

## tech stack & key tools

* **backend**: python 3.10+, fastAPI, pydantic v2
* **database & ORM**: postgreSQL, SQLAlchemy 2.0
* **security & auth**: JSON Web tokens (JWT via `python-jose`), Passlib & Bcrypt (password hashing)
* **DevOps & infrastructure**: docker, docker dompose, kubernetes (`deployment`, `service`, `nodePort`)

---

## architecture & security highlights

building a secure backend was at the core of this project. Here are a few key architectural choices:

1. **stateless JWT Authentication**: protected endpoints require a valid Bearer token provided upon login.
2. **password security**: passwords are never stored in plain text. They are hashed using `bcrypt` before hitting the database.
3. **data isolation by design**: Tasks are strictly tied to the authenticated user (`user_id` foreign Key), ensuring users can only read and manage their own data.
4. **resilient kubernetes deployment**: separate deployments and services for both the fastAPI application and postgreSQL database ensure decoupled scaling and lifecycle management.

---

### how to run the project

### option 1: quick start with docker compose (local development)

if you want to quickly spin up the environment for development or testing:

1. clone the repository and navigate to the root directory:
   ```bash
   git clone https://github.com/santspy/task-manager-api.git
   cd task-manager-api
