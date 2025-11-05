from fastapi import FastAPI
from middleware.cors import setup_cors
from api.routes import setup_routes
from repo.lifespan import lifespan 

def create_app():
    app = FastAPI(lifespan=lifespan)

    setup_cors(app)
    setup_routes(app)
    return app