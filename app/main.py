from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes.auth import router as auth_router
from .api.routes.chat import router as chat_router
from .api.routes.email import router as email_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(email_router, prefix="/email", tags=["email"])
