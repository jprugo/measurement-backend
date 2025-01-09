from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from measurement.presentation import rest as measurement_api
from configuration.presentation import rest as configuration_api
from alarming.presentation import rest as alarming_api
from worker.presentation import rest as worker_api
from option.presentation import rest as option_api

from shared_kernel.infra.container import AppContainer
from shared_kernel.infra.database.orm import init_orm_mappers

app_container = AppContainer()

app = FastAPI(
    title="Measurement Worker",
    contact={
        "name": "Gigawatt SAS",
        "email": "gigawatt-admin@gmail.com",
    },
)

app.container = app_container

origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(measurement_api.router)
app.include_router(configuration_api.router)
app.include_router(alarming_api.router)
app.include_router(worker_api.router)
app.include_router(option_api.router)

init_orm_mappers()

@app.get("/")
def health_check():
    return {"health": "200"}
