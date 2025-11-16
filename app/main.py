from fastapi import FastAPI
from app.routers import auth, quiz, result
from app.database import Base, engine

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quiz API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
app.include_router(result.router, prefix="/result", tags=["Result"])

@app.get("/")
def root():
    return {"message": "Quiz API running!"}
