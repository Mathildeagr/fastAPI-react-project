from fastapi import FastAPI
from app.models.count_table import setup_database, SessionLocal, MyTable
from fastapi.middleware.cors import CORSMiddleware

setup_database()

app = FastAPI()
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Autorise ces origines
    allow_credentials=True,
    allow_methods=["*"],        # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],        # Autorise tous les headers
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/count")
async def get_count():
    """
    Récupère la valeur de count_numbe de la première ligne.
    """
    session = SessionLocal()
    try:
        row = session.query(MyTable).first()
        if row:
            return {"count": row.count_numbe}
        return {"count": None, "message": "Aucune donnée trouvée"}
    finally:
        session.close()


@app.post("/count/increment")
async def increment_count():
    """
    Incrémente la valeur de count_numbe et retourne la nouvelle valeur.
    """
    session = SessionLocal()
    try:
        row = session.query(MyTable).first()
        if row:
            row.count_numbe += 1
            session.commit()
            session.refresh(row)  # pour récupérer la valeur mise à jour
            return {"count": row.count_numbe}
        return {"error": "Aucune ligne à incrémenter"}
    finally:
        session.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)