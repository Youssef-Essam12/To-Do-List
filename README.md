# To-Do-List
### Simple To-Do list application using FastAPI and PostgreSQL

# Setup Guide

## Prerequisites
* Docker
* Git
```bash
sudo apt update
sudo apt install docker git -y
```

## How to start the app
#### 1. Clone the Repository
```bash
    git clone https://github.com/Youssef-Essam12/To-Do-List.git
    cd To-Do-List
```

#### 2. Launch the App
Run the following command in your terminal:

```bash
docker compose up --build
```

#### 3. Access the Application through your browser
* App: http://localhost:8000
* API Docs: http://localhost:8000/docs

#### 4. To stop
* Press ```Ctrl+C```

#### 5. To remove the docker container
```bash
docker compose down
```