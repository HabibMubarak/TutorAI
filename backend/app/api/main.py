from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .endpoints import health


api = FastAPI(title="TutorAI API", version="0.0.1")

"""
Wir müssen dem Backend beibringen, dass es mit dem Frontend "reden" darf.
Browser blockieren das standardmäßig aus Sicherheitsgründen (das nennt man CORS).
"""
# Das erlaubt dem Frontend (Port 5173), auf das Backend (Port 8000) zuzugreifen.
origins = [
    "http://localhost:5137",
    "http://127.0.0.1:5137"
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api.include_router(health.router) 



@api.get("/")
def root():
    return {"message": "Welcome to the TutorAI API"}
