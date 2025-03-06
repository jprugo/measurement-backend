## Install the dependencies
```bash
pip install -r requirements.txt
```

## Run the project
```bash
uvicorn shared_kernel.infra.fastapi.main:app --host 0.0.0.0 --port 8000 --reload
```