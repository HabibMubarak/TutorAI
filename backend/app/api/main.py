from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .endpoints import health

# WICHTIG: Nenne es "app", damit uvicorn es findet!
app = FastAPI(title="TutorAI API", version="0.0.1")

# HIER WAR DER ZAHLENDREHER: 5173 statt 5137
origins = [
    "http://localhost:5173",  # <--- Korrigiert
    "http://127.0.0.1:5173"   # <--- Korrigiert
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router) 

@app.get("/")
def root():
    return {"message": "Welcome to the TutorAI API"}