from fastapi import FastAPI
from routes import user_routes, ride_routes, match_routes
from fastapi.middleware.cors import CORSMiddleware
from database.connection import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_routes.router)
app.include_router(ride_routes.router)
app.include_router(match_routes.router)