from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.boilersRouter import boilersRouter
from routers.turbinesRouter import turbineRouter
from routers.stationRouter import stationRouter

app = FastAPI()

# Добавляем middleware для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно настроить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы HTTP
    allow_headers=["*"],  # Разрешаем все заголовки HTTP
)

app.include_router(boilersRouter)
app.include_router(turbineRouter)
app.include_router(stationRouter)


