from fastapi import FastAPI
from routes import user_routes, ride_routes

from database.connection import engine, Base
from models import models  
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)
app.include_router(ride_routes.router)