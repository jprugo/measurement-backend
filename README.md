## Install the dependencies
```bash
pip install -r requirements.txt
```

## Run the project
```bash
uvicorn shared_kernel.infra.fastapi.main:app --host 0.0.0.0 --port 8000 --reload
```

## Orch container
```bash
docker network create measurements

docker compose -f ./measurement-backend/docker-compose.yml -f ./measurement-frontend/docker-compose.yml up -d

docker compose -f ./measurement-backend/docker-compose.yml  up -d
docker compose -f ./measurement-frontend/docker-compose.yml up -d
```