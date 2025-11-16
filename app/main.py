from fastapi import FastAPI
from app.routers import auth, quiz, result
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quiz API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용: 일단 다 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
app.include_router(result.router, prefix="/result", tags=["Result"])

@app.get("/")
def root():
    return {"message": "Quiz API running!"}
